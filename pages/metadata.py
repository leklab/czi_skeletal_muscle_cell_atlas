import dash
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from scripts.query import make_query

dash.register_page(__name__)


df = make_query(
    type="metadata"
    )


integration_methods = ["BBKNN", "Harmony", "Scanorama"]

layout = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.ListGroup([
                            dbc.ListGroupItem([
                                html.Label(['Select a Dataset:']),
                                html.Div(className='three columns', children=dcc.Dropdown(
                                    options=[
                                        {'label': x, 'value': x.lower()} for x in integration_methods
                                    ],
                                    value="bbknn",
                                    id='chosen_dataset',
                                    clearable=False
                                ))
                            ]),
                            dbc.ListGroupItem([
                                html.Label(['Select a Sex: ']),
                                html.Div(className='three columns', children=dcc.Dropdown(
                                    options=[
                                        {'label': 'Male', 'value': 'M'},
                                        {'label': 'Female', 'value': 'F'},
                                    ],
                                    value= 'M',
                                    id='chosen_sex',
                                    clearable=False
                                ))
                            ]),
                            dbc.ListGroupItem([
                                html.Label(['Select an Age Group: ']),
                                html.Div(className='three columns', children=dcc.Dropdown(
                                    options=[
                                        {'label': '0 - 2 yrs', 'value': '02'},
                                        {'label': '3 - 5 yrs', 'value': '35'},
                                        {'label': '6 - 12 yrs', 'value': '612'},
                                        {'label': '13 - 18 yrs', 'value': '1318'},
                                    ],
                                    value= "02",
                                    id='chosen_age',
                                    clearable=False
                                ))
                            ]),
                            dbc.ListGroupItem([
                                html.Label(['Select an Ethnicity: ']),
                                html.Div(className='three columns', children=dcc.Dropdown(
                                    options=[
                                        {'label': 'European', 'value': 'eu'},
                                        {'label': 'Non-European', 'value': 'neu'},
                                    ],
                                    value= "eu",
                                    id='chosen_ethnicity',
                                    clearable=False
                                ))
                            ]),
                            dbc.ListGroupItem([
                                html.Label(['Select a Donor: ']),
                                html.Div(className='three columns', children=dcc.Dropdown(
                                    options=[
                                        {'label': 'X', 'value': 'x'},
                                        {'label': 'Y', 'value': 'y'},
                                    ],
                                    value= "x",
                                    id='chosen_donor',
                                    clearable=False
                                ))
                            ]),
                        ], flush = False)
                    ]), width=2),
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
            ]),
            dbc.Row([
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/3yo_female_normal-control/3yo_female_H&E_40xd.jpg", width="100%"),
                    html.Div(
                        html.P("3yo Female H&E 40xd"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/3yo_female_normal-control/3yo_female_H&E_40xe.jpg", width="100%"),
                    html.Div(
                        html.P("3yo Female H&E 40xe"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/3yo_female_normal-control/3yo_female_H&E.jpg", width="100%"),
                    html.Div(
                        html.P("3yo Female H&E"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                }))
            ]),
            dbc.Row([
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/7yo_female_normal-control/7yo_normal_H&E_40xa.jpg", width="100%"),
                    html.Div(
                        html.P("7yo Female H&E 40xa"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/7yo_female_normal-control/7yo_normal_H&E_40xb.jpg", width="100%"),
                    html.Div(
                        html.P("7yo Female H&E 40xb"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/7yo_female_normal-control/7yo_normal_H&E_40xf.jpg", width="100%"),
                    html.Div(
                        html.P("7yo Female H&E 40xf"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                }))
            ]),
            dbc.Row([
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/7yo_female_normal-control/7yo_normal_H&E.jpg", width="100%"),
                    html.Div(
                        html.P("7yo Female H&E"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"assets/teenage male control muscle/teenage_male_H&E.jpg", width="100%"),
                    html.Div(
                        html.P("Teenage Male H&E"), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                })),
                dbc.Col(html.Div(className="histology", children = [
                    html.Img(src=r"", width="100%"),
                    html.Div(
                        html.P(""), 
                        style = {"textAlign":"center", "padding": "10px 20px"})
                ], 
                style = {
                    "width":"80%", 
                    "backgroundColor" : "white", 
                    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
                    "marginBottom" : "25px", 
                }))
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
    


