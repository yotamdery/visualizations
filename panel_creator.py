import dash
from dash import Input, Output, dcc
from layout import define_layout
from metric_per_score_fig_creator import create_metric_per_score_fig
from objf_per_score_fig_creator import create_objf_per_score_fig
from metric_compliant_constraints_fig_creator import create_metrics_compliant_constraints_fig

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app = define_layout(app)

# Callbacks to update the first graph based on selections - based on the app.layout
@app.callback(
    Output('metric-per-score', 'figure'),
    [Input('model-dropdown-metric', 'value'),
     Input('metric-dropdown', 'value'),
     Input('segment-dropdown-metric', 'value')]
)
def update_graph(selected_model, selected_metric, selected_segments):
    return create_metric_per_score_fig(selected_model, selected_metric, selected_segments)

# Callbacks to update the second graph based on selections - based on the app.layout
@app.callback(
    Output('objf-per-score', 'figure'),
    [Input('model-dropdown-objf', 'value'),
     Input('segment-dropdown-objf', 'value'),
     Input('scalar-x', 'value'),
     Input('scalar-y', 'value'),
     Input('scalar-z', 'value')]
)
def update_objf_per_score_graph(selected_model, selected_segments, scalar_x, scalar_y, scalar_z):
    return create_objf_per_score_fig(selected_model, selected_segments, scalar_x, scalar_y, scalar_z)


# Callbacks to update the third graph based on selections - based on the app.layout
@app.callback(
    Output('metrics-compliance', 'figure'),
    [Input('model-dropdown-metric-constraint', 'value'),
     Input('metrics-constraint-dropdown', 'value'),
     Input('segment-dropdown-metric-constraint', 'value'),
     Input('non-compliant-toggle', 'value'),
     Input('compliant-toggle', 'value'),
     Input('objf-toggle', 'value'),
     Input('scalar-x-metric', 'value'),
     Input('scalar-y-metric', 'value'),
     Input('scalar-z-metric', 'value')]
)   
        
def update_graph(selected_model: str, selected_metrics: list, selected_segments: list, 
                 filter_non_compliant: list, filter_compliant: list, show_objf: list,
                 scalar_x: float, scalar_y: float, scalar_z: float):
    return create_metrics_compliant_constraints_fig(selected_model, selected_metrics, selected_segments, 
                                                    filter_non_compliant, filter_compliant, show_objf,
                                                    scalar_x, scalar_y, scalar_z)

## Callbacks to update the additional forth graph based on selections - based on the app.layout
# Callbacks to toggle the visibility of additional inputs
@app.callback(
    Output('additional-figure-inputs', 'style'),
    Input('show-figure', 'value')
)
def toggle_additional_inputs(show_figure):
    if 'show' in show_figure:
        return {'display': 'block'}
    return {'display': 'none'}

# Callbacks to update the additional fourth graph based on selections - based on the app.layout
@app.callback(
    Output('figure-container', 'children'),
    [Input('show-figure', 'value'),
     Input('model-dropdown-metric-constraint-2', 'value'),
     Input('metrics-constraint-dropdown-2', 'value'),
     Input('segment-dropdown-metric-constraint-2', 'value'),
     Input('non-compliant-toggle-2', 'value'),
     Input('compliant-toggle-2', 'value'),
     Input('objf-toggle-2', 'value'),
     Input('scalar-x-metric-2', 'value'),
     Input('scalar-y-metric-2', 'value'),
     Input('scalar-z-metric-2', 'value')]
)

def update_additional_figure(show_figure, selected_model: str, selected_metrics: list, 
                             selected_segments: list, filter_non_compliant: list, filter_compliant: list, show_objf: list,
                             scalar_x: float, scalar_y: float, scalar_z: float):
    if 'show' in show_figure:
        fig = create_metrics_compliant_constraints_fig(selected_model, selected_metrics, selected_segments, 
                                                       filter_non_compliant, filter_compliant, show_objf,
                                                       scalar_x, scalar_y, scalar_z)
        return [dcc.Graph(id='metrics-compliance-2', figure=fig)]
    return []

    
# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)