import dash
from dash import html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# the global dash app

app = None


def serve_layout():
    global app

    layout = dbc.Container([dbc.Row([dbc.Col(html.Div("Hello World")),
                                     dbc.Col(dbc.Button("Press Me", id='my-button'))
                                     ]),
                            dbc.Row([dbc.Col(html.Div("This is a dash app")),
                                     dbc.Col(html.Div(id="button-message"))
                                     ]),
                           ])
    return layout


@callback(Output('button-message', 'children'),
          Input('my-button', 'n_clicks'))
def button_callback(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        message = f"The button has been pressed {n_clicks} times"
    else:
        message = ''
    return message


def run_app():
    app = dash.Dash("My Dash App",
                    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                    url_base_pathname='/my-dash-app/')

    app.layout = serve_layout()

    app.run_server(debug=True,
                   host='localhost',
                   port=1854)


if __name__ == '__main__':
    # get command line parameters here

    run_app()
