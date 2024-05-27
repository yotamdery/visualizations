from dash import html, dcc
from data_reader import df_no_constraints, df_after_constraints

def define_layout(app):
    app.layout = html.Div([
        html.H1("Interactive Dashboard", style={
            'textAlign': 'center',
            'background': 'linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%)',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent',
            'margin': '10px auto',
            'fontSize': '5em'  # Larger font size for impact
            }),
        html.Div([  # Outer container for layout structure
            # Container for the first graph and its controls
            html.Div([  
                html.H2("Metric Value Per Score", style={
                    'textAlign': 'center',
                    'WebkitBackgroundClip': 'text',
                    'margin': '10px auto',
                    'fontSize': '2em'  # Larger font size for impact
                }),
                html.Label("Select Model"),
                dcc.Dropdown(
                    id='model-dropdown-metric',
                    options=[{'label': col, 'value': col} for col in [
                        'RMR_MODEL_LOGIN_1_model_score1', 'login22_score'
                    ]],
                    value='RMR_MODEL_LOGIN_1_model_score1',
                    style={'width': '40%', 'marginBottom': '10px'}  # Adds spacing below the dropdown
                ),
                html.Label("Select Metric"),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': col, 'value': col} for col in [
                        'prevention_rate', 'bad_rate', 'goods_actioned', 'accuracy', 'num_of_sessions_total'
                    ]],
                    value='prevention_rate',
                    style={'width': '40%', 'marginBottom': '10px'}  
                ),
                html.Label("Select Segments"),
                dcc.Dropdown(
                    id='segment-dropdown-metric',
                    options=[{'label': segment, 'value': segment} for segment in df_no_constraints['opt_segment'].unique()],
                    multi=True,
                    placeholder="Select one or more segments",  # Placeholder text when nothing is selected
                    style={'width': '40%', 'marginBottom': '20px'}
                ),
                dcc.Graph(id='metric-per-score')
            ], style={'width': '99%', 'padding': '20px'}),  # Full width and some padding for aesthetics

            # Container for the second graph and its controls
            html.Div([  
                html.H2("Objective Function Value per Score", style={
                    'textAlign': 'center',
                    'WebkitBackgroundClip': 'text',
                    'margin': '10px auto',
                    'fontSize': '2em'  # Larger font size for impact
                }),
                html.Label("Select Model"),
                dcc.Dropdown(
                    id='model-dropdown-objf',
                    options=[{'label': col, 'value': col} for col in [
                        'RMR_MODEL_LOGIN_1_model_score1', 'login22_score'
                    ]],
                    value='RMR_MODEL_LOGIN_1_model_score1',
                    style={'width': '40%', 'marginBottom': '10px'}
                ),
                dcc.Dropdown(
                    id='segment-dropdown-objf',
                    options=[{'label': segment, 'value': segment} for segment in df_after_constraints['opt_segment'].unique()],
                    multi=True,
                    placeholder="Select one or more segments",  # Placeholder text when nothing is selected
                    style={'width': '40%', 'marginBottom': '20px'}
                ),
                dcc.Graph(id='objf-per-score')
            ], style={'width': '99%', 'padding': '20px'}),  # Full width and some padding for aesthetics

            # Container for the third graph and its controls
            html.Div([  
                html.H2("Metrics Compliance To Constraint", style={
                    'textAlign': 'center',
                    'WebkitBackgroundClip': 'text',
                    'margin': '10px auto',
                    'fontSize': '2em'  # Larger font size for impact
                }),
                html.Label("Select Model"),
                dcc.Dropdown(
                    id='model-dropdown-metric-constraint',
                    options=[{'label': col, 'value': col} for col in [
                        'RMR_MODEL_LOGIN_1_model_score1', 'login22_score'
                    ]],
                    value='RMR_MODEL_LOGIN_1_model_score1',
                    style={'width': '40%', 'marginBottom': '10px'}  # Adds spacing below the dropdown
                ),
                html.Label("Select Metrics"),
                dcc.Dropdown(
                    id='metrics-constraint-dropdown',
                    options=[{'label': col, 'value': col} for col in [
                        'prevention_rate', 'bad_rate', 'goods_actioned', 'accuracy', 'num_of_sessions_total'
                    ]],
                    multi=True,
                    style={'width': '40%', 'marginBottom': '10px'}  
                ),
                html.Label("Select Segments"),
                dcc.Dropdown(
                    id='segment-dropdown-metric-constraint',
                    options=[{'label': segment, 'value': segment} for segment in df_no_constraints['opt_segment'].unique()],
                    multi=True,
                    placeholder="Select one or more segments",  # Placeholder text when nothing is selected
                    style={'width': '40%', 'marginBottom': '20px'}
                ),
                dcc.Checklist(
                    id='non-compliant-toggle',
                    options=[
                        {'label': 'Show only non-compliant candidates', 'value': 'show_non_compliant'}
                    ],
                    value=[]  # Initially unchecked
                ),
                dcc.Checklist(
                    id='compliant-toggle',
                    options=[
                        {'label': 'Show only compliant candidates', 'value': 'show_compliant'}
                    ],
                    value=[],  # Initially unchecked
                    style={'marginBottom': '10px'}
                ),
                dcc.Checklist(
                    id='objf-toggle',
                    options=[
                        {'label': 'Show Objective Function', 'value': 'show_objective_function'}
                    ],
                    value=['show_objective_function'],  # Initially unchecked
                    style={'marginBottom': '10px'}
                ),
                dcc.Graph(id='metrics-compliance')
            ], style={'width': '99%', 'padding': '20px'}),  # Full width and some padding for aesthetics

        # Fourth and additional figure if wanted by the user
        html.Div([
            dcc.Checklist(
                id='show-figure',
                options=[{'label': 'Show Additional Figure', 'value': 'show'}],
                value=[],
                inline=True
            ),
            html.Div(id='figure-container', children=[]),
            # Second graph input components
            html.Div(id='additional-figure-inputs', children=[
                html.Label("Select Model"),
                dcc.Dropdown(
                    id='model-dropdown-metric-constraint-2',
                    options=[{'label': col, 'value': col} for col in [
                        'RMR_MODEL_LOGIN_1_model_score1', 'login22_score'
                    ]],
                    value='RMR_MODEL_LOGIN_1_model_score1',
                    style={'width': '40%', 'marginBottom': '10px'}  # Adds spacing below the dropdown
                ),
                html.Label("Select Metrics"),
                dcc.Dropdown(
                    id='metrics-constraint-dropdown-2',
                    options=[{'label': col, 'value': col} for col in [
                        'prevention_rate', 'bad_rate', 'goods_actioned', 'accuracy', 'num_of_sessions_total'
                    ]],
                    multi=True,
                    style={'width': '40%', 'marginBottom': '10px'}  
                ),
                html.Label("Select Segments"),
                dcc.Dropdown(
                    id='segment-dropdown-metric-constraint-2',
                    options=[{'label': segment, 'value': segment} for segment in df_no_constraints['opt_segment'].unique()],
                    multi=True,
                    placeholder="Select one or more segments",  # Placeholder text when nothing is selected
                    style={'width': '40%', 'marginBottom': '20px'}
                ),
                dcc.Checklist(
                    id='non-compliant-toggle-2',
                    options=[
                        {'label': 'Show only non-compliant candidates', 'value': 'show_non_compliant'}
                    ],
                    value=[]  # Initially unchecked
                ),
                dcc.Checklist(
                    id='compliant-toggle-2',
                    options=[
                        {'label': 'Show only compliant candidates', 'value': 'show_compliant'}
                    ],
                    value=[],  # Initially unchecked
                    style={'marginBottom': '10px'}
                ),
                dcc.Checklist(
                    id='objf-toggle-2',
                    options=[
                        {'label': 'Show Objective Function', 'value': 'show_objective_function'}
                    ],
                    value=['show_objective_function'],  # Initially unchecked
                    style={'marginBottom': '10px'}
                ),
                dcc.Graph(id='metrics-compliance-2')
            ], style={'display': 'none'})  # Initially hidden
    
            ])
        ])
    ])
    return app

def update_fig_layout(fig, title: str):
    """ An inner function to encapsulate the layout update """
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Centers the title
            'y': 0.92,
            'xanchor': 'center'
        },
        title_font=dict(size=24),  # Main title font size
        xaxis_title_font=dict(size=18),  # X-axis title font size
        yaxis_title_font=dict(size=18),  # Y-axis title font size
        font=dict(size=14),  # General font size for other annotations like ticks and legends
        xaxis=dict(range=[0, None])
    )
    return fig