from dash import Dash, dcc, html
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

from components.navbar import navbar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)

if not os.path.exists("images"):
    os.mkdir("images")

axis_template = {
    "showbackground": True,
    "backgroundcolor": "#rgb(255, 255, 255)",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}

app.layout = html.Div([
	navbar,
	dash.page_container
])


if __name__ == __name__:
    app.run_server(debug=True)


