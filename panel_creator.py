import dash
from dash import Input, Output
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
     Input('segment-dropdown-objf', 'value')]
)

def update_graph(selected_model, selected_segments):
    return create_objf_per_score_fig(selected_model, selected_segments)


#Callbacks to update the third graph based on selections - based on the app.layout
@app.callback(
    Output('metrics-compliance', 'figure'),
    [Input('model-dropdown-metric-constraint', 'value'),
     Input('metrics-constraint-dropdown', 'value'),
     Input('segment-dropdown-metric-constraint', 'value'),
     Input('non-compliant-toggle', 'value'),
     Input('compliant-toggle', 'value'),
     Input('objf-toggle', 'value')]
)   
        
def update_graph(selected_model: str, selected_metrics: list, selected_segments: list, filter_non_compliant: list, filter_compliant: list, show_objf: list):
    return create_metrics_compliant_constraints_fig(selected_model, selected_metrics, selected_segments, filter_non_compliant, filter_compliant, show_objf)

    
# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)