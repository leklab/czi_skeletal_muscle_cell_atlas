import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

from scripts.img_grid import generate_grid
from components.options import histology_options

dash.register_page(__name__)

layout = html.Div([
        dbc.Row([
            html.Div([
                dbc.Col(
                    html.Div([
                        dbc.Row(html.H4("Histology Metadata")),
                        dbc.Row(html.P("Filter histology slides. Click on an image to view an enlarged version."))
                    ])
                ),
                dbc.Col(
                    dbc.Button("Export", id="histology_export", n_clicks=0)
                ),
                html.Div(id="test")
            ], style={'justify-content': 'space-between'})
        ]),
        dbc.Row([
            dbc.Col(histology_options(), width = 2),
            dbc.Col(id = "histology_grid"),
            html.Div(id='modal', children=[
                html.Img(
                    src="assets/3yo_female_normal-control/3yo_female_H&E_40xd.jpg",
                    height='500',
                    width='500',
                    style={
                        'display':'block',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }
                )
            ], style={'display': 'none'})
        ]),
    ], style={
        'margin-left': '5%', 
        'margin-right': '5%', 
        'overflow-x': 'hidden'
    })

@callback(
    Output('histology_grid', 'children'),
    Input('chosen_sex', 'value'),
    Input('chosen_age', 'value'),
    Input('chosen_stain', 'value'),
    Input('image-slider', 'value')
)
def filter_images(sex, age, stain, slider):
    histology_images = pd.read_csv('data/histology.csv')
    filtered = histology_images

    if (sex != "All"):
        filtered = histology_images[histology_images["sex"] == sex]

    if (age != "All"):
        filtered = histology_images[histology_images["age_group"] == age]
    
    if (stain != "All"):
        filtered = histology_images[histology_images["staining_method"] == stain]

    res = list(map(
        lambda x: (
            "assets/" + x, 
            x.split("/")[1].split(".")[0].replace("_", " ")
        ), 
        filtered["src"]
    ))

    return generate_grid(res, slider)

# Enlarges image
@callback(
    Output('modal', 'style'),
    Input('enlarge-image-1', 'n_clicks'),
    prevent_initial_call = True,
)
def display_image(n):
    return {
            'display': 'block',
            'z-index': '1',
            'padding-top': '100',
            'left': '0',
            'top': '0',
            'width': '100%',
            'height': '100%',
            'overflow': 'auto'
        } if n % 2 == 0 else {'display': 'none'}

@callback(
    Output("test", "children"),
    Input("histology_export", "n_clicks"),
    prevent_initial_call=True,
)
def download_exp_handler(click):
    if click:
        print("hello")