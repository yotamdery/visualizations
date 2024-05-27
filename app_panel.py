import panel as pn
import pandas as pd
import hvplot.pandas

# Load data
df = pd.read_csv("visualizations/data/candidates_perf_raw.csv")

# Set up Panel widgets
model_options = ['RMR_MODEL_LOGIN_1_model_score1', 'login22_score']
metric_options = ['prevention_rate', 'bad_rate', 'goods_actioned', 'accuracy', 'num_of_sessions_total']

model_select = pn.widgets.Select(name='Select Model', options=model_options)
metric_select = pn.widgets.Select(name='Select Metric', options=metric_options)

# Function to update the graph
def update_plot(event=None):
    selected_model = model_select.value
    selected_metric = metric_select.value
    plot = df.hvplot.scatter(x=selected_model, y=selected_metric, by='opt_segment', size=5, responsive=True)
    return plot

# Attach the update function to widget events
model_select.param.watch(update_plot, 'value')
metric_select.param.watch(update_plot, 'value')

# Initial plot
plot = update_plot()

# Layout
layout = pn.Column(
    pn.Row(model_select, metric_select),
    plot
)

# Show the dashboard
pn.serve(layout)