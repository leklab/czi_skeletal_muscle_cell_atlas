"""
Sets up a web application using the Dash framework.
"""

import os

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

from components.navbar import navbar

if not os.path.exists("images"):
    os.mkdir("images")

load_dotenv()

app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    use_pages=True, 
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
	navbar,
	dash.page_container,
])

if __name__ == __name__:
    app.run_server(debug=True)


