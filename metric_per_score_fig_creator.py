import plotly.express as px
from layout import update_fig_layout
from data_reader import df_no_constraints

def create_metric_per_score_fig(selected_model, selected_metric, selected_segments):
    if selected_segments:  # This check is now safe because selected_segments will not be None or empty
        filtered_df = df_no_constraints[df_no_constraints['opt_segment'].isin(selected_segments)]
        fig = px.line(filtered_df, x=selected_model, y=selected_metric, color='opt_segment', markers=True)
        selected_metric = selected_metric.replace('_', ' ').capitalize()
        fig = update_fig_layout(fig, title=f'{selected_metric} Value per Score')
    else:
        # If no segments are initially selected, display a blank figure
        fig = px.scatter(title="Please select segments from the dropdown.")
        fig.update_layout(title="No segments selected. Please select segments from the dropdown.")
    return fig