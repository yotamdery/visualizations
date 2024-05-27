import pandas as pd 
import numpy as np
import itertools, re
import plotly.graph_objects as go
from plotly.colors import qualitative
from data_reader import df_no_constraints, login_limits

def create_metrics_compliant_constraints_fig(selected_model: str, selected_metrics: list, selected_segments: list, filter_non_compliant: list, filter_compliant: list, show_objf: list):
    if selected_segments and selected_metrics: 
        # Plot object definition 
        fig = go.Figure()
        # Color assignment - get a list of distinct colors and use the same color for each segment across metrics
        colors = qualitative.Plotly
        segment_colors = {(segment, metric): colors[i % len(colors)] for i, (segment, metric) in enumerate(itertools.product(selected_segments, selected_metrics))}

        # Getting the relevant data based on chosen segments, metrics and constraints
        filtered_df = get_filtered_df(df_no_constraints, selected_segments, selected_metrics, selected_model, filter_non_compliant, filter_compliant)

        if filtered_df.empty:
            # If no segments and metrics are initially selected, display a blank figure
            fig = go.Figure(layout=go.Layout(title=""))
            fig.update_layout(title="No data to show. Please choose different settings")
            return fig

        # Single segment, multiple metrics
        if len(selected_segments) == 1 and len(selected_metrics) > 1:
            segment = selected_segments[0]
            for metric in selected_metrics:
                fig.add_trace(go.Scatter(
                    x=filtered_df[selected_model],
                    y=filtered_df[metric],
                    mode='markers',
                    name=f"{segment} - {metric}",
                    hovertemplate=(
                            "<b>%{fullData.name}</b><br>" +
                            "Model Score: %{x}<br>" +
                            "Metric Value: %{y}<br>" +
                            "<extra></extra>"  # Hides the trace info
                        )
                ))
                
        # Single metric, multiple segments
        elif len(selected_metrics) == 1 and len(selected_segments) > 1:
            metric = selected_metrics[0]
            for segment in selected_segments:
                segment_df = filtered_df[filtered_df['opt_segment'] == segment]
                fig.add_trace(go.Scatter(
                    x=segment_df[selected_model],
                    y=segment_df[metric],
                    mode='markers',
                    name=segment,
                    line=dict(color=segment_colors[(segment, metric)]),
                    hovertemplate=(
                            "<b>%{fullData.name}</b><br>" +
                            "Model Score: %{x}<br>" +
                            "Metric Value: %{y}<br>" +
                            "<extra></extra>"  # Hides the trace info
                        )
                ))

        else:
            # Multiple segments and metrics
            for segment in selected_segments:
                segment_df = filtered_df[filtered_df['opt_segment'] == segment]
                for metric in selected_metrics:
                    fig.add_trace(go.Scatter(
                        x=segment_df[selected_model],
                        y=segment_df[metric],
                        mode='markers',
                        name=f"{segment} - {metric}",
                        line=dict(color=segment_colors[(segment, metric)]),
                        # Customizing hover information
                        hovertemplate=(
                            "<b>%{fullData.name}</b><br>" +
                            "Model Score: %{x}<br>" +
                            "Metric Value: %{y}<br>" +
                            "<extra></extra>"  # Hides the trace info
                        )
                    ))
        
        # Add horizontal lines to the figure, according to the boundries
        add_horizontal_lines(fig, get_boundaries(selected_metrics, selected_segments), selected_model, segment_colors)
        if 'show_objective_function' in show_objf:
            plot_objf_trend(fig, filtered_df, selected_model, selected_segments)
        fig = update_fig_layout(fig, title='Compliant to Constraints', xaxis_title=selected_model, yaxis_title='Metrics Value')
        
    else:
        # If no segments and metrics are initially selected, display a blank figure
        fig = go.Figure(layout=go.Layout(title=""))
        fig.update_layout(title="No segments and metric selected. Please select segments and metrics from the dropdowns.")

    return fig


def get_filtered_df(df: pd.DataFrame, selected_segments: list, selected_metrics: list, selected_model: str, filter_non_compliant: list, filter_only_compliant: list) -> pd.DataFrame:
    filtered_df = df[df['opt_segment'].isin(selected_segments)]
    
    # Algorithm for cases where only the "Show only non-compliant candidates" box is checked.
    if 'show_non_compliant' in filter_non_compliant and 'show_compliant' not in filter_only_compliant:
        boundaries = get_boundaries(selected_metrics, selected_segments)
        non_compliant_mask = pd.Series(False, index=filtered_df.index)  # Use DataFrame index to avoid misalignment

        for segment in selected_segments:
            segment_df = filtered_df[filtered_df['opt_segment'] == segment]
            segment_non_compliant_mask = pd.Series(False, index=segment_df.index)  # Use segment DataFrame index

            for metric in selected_metrics:
                metric_lower = f"{metric}_lower"
                metric_upper = f"{metric}_upper"
                lower_bound = boundaries.at[segment, metric_lower] if metric_lower in boundaries.columns else float('-inf')
                upper_bound = boundaries.at[segment, metric_upper] if metric_upper in boundaries.columns else float('inf')

                # Apply non-compliant conditions
                metric_non_compliant_mask = ((segment_df[metric] < lower_bound) & np.isfinite(lower_bound)) | \
                                            ((segment_df[metric] > upper_bound) & np.isfinite(upper_bound))

                segment_non_compliant_mask |= metric_non_compliant_mask  # Ensure correct logical OR operation
            non_compliant_mask |= segment_non_compliant_mask  # Update the overall mask correctly

        filtered_df = filtered_df[non_compliant_mask]  # Apply the mask to filter the DataFrame

        if filtered_df[selected_model].isna().all():
            return pd.DataFrame()
        
    # Algorithm for cases where only the "Show only compliant candidates" box is checked.
    elif 'show_compliant' in filter_only_compliant and 'show_non_compliant' not in filter_non_compliant:
        boundaries = get_boundaries(selected_metrics, selected_segments)
        compliant_mask = pd.Series(True, index=filtered_df.index)  # Correct indexing
        
        for segment in selected_segments:
            segment_df = filtered_df[filtered_df['opt_segment'] == segment]
            segment_compliant_mask = pd.Series(True, index=segment_df.index)  # Ensure index alignment
            
            for metric in selected_metrics:
                metric_lower = f"{metric}_lower"
                metric_upper = f"{metric}_upper"
                lower_bound = boundaries.at[segment, metric_lower] if metric_lower in boundaries.columns else float('-inf')
                upper_bound = boundaries.at[segment, metric_upper] if metric_upper in boundaries.columns else float('inf')

                # Correcting the boundary check logic
                metric_compliant_mask = (segment_df[metric] >= lower_bound) & (segment_df[metric] <= upper_bound)
                segment_compliant_mask &= metric_compliant_mask  # Correct application of the mask

            compliant_mask &= segment_compliant_mask  # Update the overall mask
        filtered_df = filtered_df[compliant_mask]

        # Check if the resulting DataFrame is empty or all selected_model values are NaN
        if filtered_df.empty or filtered_df[selected_model].isna().all():
            return pd.DataFrame()

    return filtered_df


def add_horizontal_lines(fig, boundaries: pd.DataFrame, selected_model: str, segment_colors: dict) -> None:
    # Assuming each column in boundaries_df is a metric and rows are 'lower' and 'upper' bounds
    for segment in boundaries.index:
        for col in boundaries.columns:
            value = boundaries.at[segment, col]
            if np.isfinite(value):
                # Retrieve color for the specific segment and metric
                color = segment_colors.get((segment, re.sub(r"_(lower|upper)$", "", col)), 'black')  # Fallback to black if not found
                # Assuming metric names are embedded in column names as '<metric>_lower' or '<metric>_upper'
                metric = col.split('_')[0]

                # Create x values for the full range of the model data
                x_values = np.linspace(df_no_constraints[selected_model].min(), 
                                       df_no_constraints[selected_model].max(), 
                                       num=100)  # Fixed number of points for line

                # Adding the horizontal line to the plot
                fig.add_trace(go.Scatter(
                    x=x_values, 
                    y=[value] * len(x_values),
                    mode='lines',
                    line=dict(color=color, width=2, dash='dash'),
                    name=f'{metric} {col.split("_")[1]}',  # E.g., 'accuracy lower'
                    showlegend=False,
                    hoverinfo='text',
                    hovertext=f'{segment}: {metric} {col.split("_")[1]} threshold: {value}'  # Detailed hover text
                ))


def plot_objf_trend(fig, df: pd.DataFrame, selected_model: str, selected_segments: list) -> None:
    for segment in selected_segments:
        segment_df = df[df['opt_segment'] == segment]
        
        fig.add_trace(go.Scatter(
            x=segment_df[selected_model],
            y=segment_df['objf'],
            mode='lines+markers',
            name=f'Objective Function of {segment}',
            line=dict(color='black'),
            hovertemplate=(
                    f"<b>{segment}</b><br>" +
                    "Objective Function: %{y}<br><extra></extra>"
                    )
        ))                

def get_boundaries(selected_metrics: str, selected_segments) -> pd.DataFrame:
    # Get the relevant row from the limits df
    limits_by_segment = login_limits.set_index('opt_segment').loc[selected_segments]
    # Omit the 'datatype' value from the DF
    filtered_limits_df = limits_by_segment[[col for col in limits_by_segment.columns if col != 'datatype']]
    # Filtering the DataFrame columns
    filtered_df = filtered_limits_df[[col for col in filtered_limits_df.columns if any(col.startswith(prefix) for prefix in selected_metrics)]]
    return filtered_df

def update_fig_layout(fig, title: str, xaxis_title: str, yaxis_title: str):
    """ An inner function to encapsulate the layout update """
    fig.update_layout(
        title={
            'text': title,
            'x': 0.46,  # Centers the title
            'y': 0.92,
            'xanchor': 'center'
        },
        xaxis=dict(
            range=[0, None],
            title = xaxis_title,
            title_font=dict(size=18)
            ),
        yaxis=dict(
            title = yaxis_title,
            title_font=dict(size=18)
            ),

        title_font=dict(size=24),  # Main title font size
        font=dict(size=14)  # General font size for other annotations like ticks and legends        
    )
    return fig