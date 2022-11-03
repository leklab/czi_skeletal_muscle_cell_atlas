import dash
from dash import html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from scripts.query import make_query
from components.options import histology_options, metadata_options

dash.register_page(__name__)

images = [
    ("assets/3yo_female_normal-control/3yo_female_H&E_40xd.jpg", "3yo Female H&E 40xd"), 
    ("assets/3yo_female_normal-control/3yo_female_H&E_40xe.jpg", "3yo Female H&E 40xe"),
    ("assets/3yo_female_normal-control/3yo_female_H&E.jpg", "3yo Female H&E"),
    ("assets/7yo_female_normal-control/7yo_normal_H&E_40xa.jpg", "7yo Female H&E 40xa"),
    ("assets/7yo_female_normal-control/7yo_normal_H&E_40xb.jpg", "7yo Female H&E 40xb"),
    ("assets/7yo_female_normal-control/7yo_normal_H&E_40xf.jpg", "7yo Female H&E 40xf"),
    ("assets/7yo_female_normal-control/7yo_normal_H&E.jpg", "7yo Female H&E"),
    ("assets/teenage male control muscle/teenage_male_H&E.jpg", "Teenage Male H&E"),
]

def generate_grid (lst):
    m, n = 2, 4
    imageSquares = []
    count = 0
    for _ in range(m):
        tmp = []
        for _ in range(n):
            tmp.append(imageSquare(lst[count][0], lst[count][1]))
            count += 1
        imageSquares.append(tmp)
    
    res = []
    for i in imageSquares:
        res.append(dbc.Row(i))
    return res

def imageSquare(src, alt, num=0):
    return dbc.Col(children = [
        html.Div(className="histology", children = [
            html.Img(src=src, width="100%", style = {"cursor": "pointer"}, id = f"test-image-{num}"),
            html.Div(
                html.P(alt), 
                style = {"textAlign":"center", "padding": "10px 20px"}),
            ], 
            style = {
                "width":"95%", 
                "backgroundColor" : "white", 
                "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                "marginBottom" : "25px"
            }
        ),
        html.Div(id='modal', children=[
            html.Img(
                src=src,
                height='500',
                width='500',
                style={
                    'display':'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                })
        ], style={'display': 'none'})
    ])

df = make_query(type="metadata")

layout = html.Div([
            dbc.Row(html.H4("Histology Metadata")),
            dbc.Row(html.P("Filter histology slides. Click on an image to view an enlarged version.")),
            dbc.Row([
                dbc.Col(histology_options(), width = 2),
                dbc.Col(children = generate_grid(images))
            ]),
            dbc.Row(html.H4("Donor Metadata")),
            dbc.Row([
                    dbc.Col(metadata_options() , width=2),
                    dbc.Col(html.Div(className="visualizations", children=[
                        dbc.Row([
                            dbc.Col([
                                dash_table.DataTable(
                                df.to_dict('records'),
                                [{"name": i, "id": i} for i in df.columns],
                                page_size=25,
                                style_table={'width': '40%'},
                                style_cell={'textAlign': 'left'},
                                id = 'metadata_table'
                            )], width=6),
                        ]),
                    ])),
                ])
        ], style={'margin-left': '5%', 'margin-right': '5%', 'overflow-x': 'hidden'})



@callback(
    Output('metadata_table', 'data'),
    Input('chosen_dataset', 'value'),
    Input('chosen_sex', 'value'),
    Input('chosen_age', 'value'),
    Input('chosen_ethnicity', 'value')
)
def update_table(dataset_value, sex_value, age_value, ethnicity_value):
    
    #Placeholder code
    df = make_query(
        type="metadata"
        )

    return df.to_dict('records')

# Enlarges image
@callback(
    Output('modal', 'style'),
    [Input('test-image-1', 'n_clicks')],
    prevent_initial_call = True,
)
def display_image(n):
    if n % 2 == 0:
        return {'display': 'none'}
    else:
        return {
            'display': 'block',
            'z-index': '1',
            'padding-top': '100',
            'left': '0',
            'top': '0',
            'width': '100%',
            'height': '100%',
            'overflow': 'auto'
            }