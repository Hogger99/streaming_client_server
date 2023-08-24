import dash
import requests
from dash import dcc, ctx
from dash import html, Input, Output
import time
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Main Page"),
    html.Button("Button 1", id="button-1", n_clicks=0),
    html.Button("Button 2", id="button-2", n_clicks=0),
    html.Button("Button 3", id="button-3", n_clicks=0),
    html.Button("Button 4", id="button-4", n_clicks=0),
    dcc.Loading(
        id="loading-component",
        type="default",
        children=[html.Div(id="output-message")]
    ),
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="output"),

    dbc.Form(
        dbc.Row(
            [
                dbc.Label("name", width="auto"),
                dbc.Col(
                    dbc.Input(type="name", id="name-input", placeholder="Enter name"),
                    className="me-3",
                ),
                dbc.Label("age", width="auto"),
                dbc.Col(
                    dbc.Input(type="age", id="age-input", placeholder="Enter age"),
                    className="me-3",
                ),
                dbc.Col(dbc.Button("Submit", id="submit-button", color="primary"), width="auto"),
            ],
            className="g-2",
        )
    )
])

"""
app.layout = dbc.Container([dbc.Row([dbc.Col(html.H1("Main Page"))]),
                            dbc.Row([dbc.Col(dbc.Button("Button 1", id="button-1", n_clicks=0)),
                                     dbc.Col(dbc.Button("Button 2", id="button-2", n_clicks=0)),
                                     dbc.Col(dbc.Button("Button 3", id="button-3", n_clicks=0)),
                                     dbc.Col(dbc.Button("Button 4", id="button-4", n_clicks=0))]),
                            dbc.Row([dcc.Loading(id="loading-component",
                                                 type="default",
                                                 children=[html.Div(id="output-message")]
                                                 )
                                     ]
                                    )
                           ]
                           )

"""


@app.callback(
    dash.dependencies.Output("output-message", "children"),
    [
        dash.dependencies.Input("submit-button", "n_clicks"),
        dash.dependencies.State("name-input", "value"),
        dash.dependencies.State("age-input", "value")
    ]
)
def submit_name_age(n_clicks, name, age):
    if n_clicks is not None and n_clicks > 0:
        url = "http://localhost:18022/api/v1/query_relational_data"
        params = {'key': ' ', 'value': " ", 'name': name, 'age': int(age)}
        headers = {'Content-Type': 'application/json'}
        records = []
        error = None
        r = requests.post(url=url, params=params, headers=headers)
        if r.status_code == 200:
            records = r.json()
        else:
            error = r.text
        message = f"{records}, {error}"
    else:
        message = ""
    return message

def update_output(bt1_click, bt2_click, bt3_click, bt4_click):

    context_id = ctx.triggered_id
    if context_id == "button-1":
        return f"Button 1 clicked {bt1_click} times."
    elif context_id == "button-2":
        return f"Button 2 clicked {bt2_click} times."
    elif context_id == "button-3":
        return f"Button 3 clicked {bt3_click} times."
    elif context_id == "button-4":
        return f"Button 4 clicked {bt4_click} times."
    else:
        return ""

if __name__ == "__main__":
    app.run_server(debug=True)
