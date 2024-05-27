import plotly.express as px
import pandas as pd 
from layout import update_fig_layout
from data_reader import df_after_constraints


def create_objf_per_score_fig(selected_model, selected_segments):
    if selected_segments:  # This check is now safe because selected_segments will not be None or empty
        filtered_df = df_after_constraints[df_after_constraints['opt_segment'].isin(selected_segments)]
        fig = px.line(filtered_df, x=selected_model, y='objf', color='opt_segment', markers=True)
        fig = update_fig_layout(fig, title='Objective Function Value per Score')
    else:
        # If no segments are initially selected, display a blank figure
        fig = px.scatter(title="Please select segments from the dropdown.")
        fig.update_layout(title="No segments selected. Please select segments from the dropdown.")
    
    return fig