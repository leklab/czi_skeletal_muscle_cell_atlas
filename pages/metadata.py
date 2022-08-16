import dash
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
import requests
import json
from PIL import Image

from scripts.process_gene_id import get_gene_id
from scripts.query import make_query
from components.download import download_modal

dash.register_page(__name__)
url = 'http://35.223.25.228/api/'

query = """{
      metadata_point{
        cell_id
        age
        sex
      }
    }
    """

r = requests.post(url, data={'query': query})
mstr = r.text
df = pd.DataFrame(json.loads(mstr)['data']['metadata_point'])
print(df)

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

                ]), width=10),
                dbc.Col([
                    html.Img(src=r'assets/histology_slides/histology.jpg'),
                    html.Img(src=r'assets/histology_slides/histology_2.jpeg'),
                    html.Img(src=r'assets/histology_slides/histology_3.jpg'),
                ])
                ])
            ])


@callback(
    Output('metadata_table', 'data'),
    Input('chosen_dataset', 'value'),
    Input('chosen_sex', 'value'),
    Input('chosen_age', 'value'),
    Input('chosen_ethnicity', 'value')
)
def update_table(dataset_value, sex_value, age_value, ethnicity_value):

    query = f"""{{
          metadata_point{{
            cell_id
            age
            {sex_value}
          }}
        }}
        """

    r = requests.post(url, data={'query': query})
    mstr = r.text

    df = pd.DataFrame(json.loads(mstr)['data']['metadata_point'])

    table = dash_table.DataTable(
        df.to_dict('records'),
        [{"name": i, "id": i} for i in df.columns],
        page_size=25,
        style_table={'width': '40%'},
        style_cell={'textAlign': 'left'},
        id='metadata_table')

    return table
