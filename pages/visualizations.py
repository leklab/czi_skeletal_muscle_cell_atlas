import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

from scripts.process_gene_id import get_gene_id
from scripts.query import make_query
from components.download import download_modal

colors = {
    'text': '#000000'
}

# Options
# genes = get_gene_id("gene_names.tsv")
with open("genes.tsv") as gene:
    genes = [line.strip("\n") for line in gene]
    gene.close()

metadata_feature = ["source","sample", "chemistry", "injury days", "injury agent", "age", "type", 
"tissue", "mouse strain", "sex", "mice per sample", "sequencing instrument"]
integration_methods = ["BBKNN", "Harmony", "Scanorama"]

dash.register_page(__name__, path="/")

layout = html.Div([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Label(['Select a Gene: ']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in genes
                        ],
                        value="Thoc1",
                        id='chosen_gene',
                        clearable=False
                    ))
                ]),
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
                    html.Label(['Select a Feature: ']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in metadata_feature
                        ],
                        value= "source",
                        id='chosen_feature',
                        clearable=False
                    ))
                ])
            ], flush = False)
        ]), width=2),
        dbc.Col(html.Div(className="visualizations", children = [
            dbc.Tabs(id = "chosen_model", active_tab= "UMAP", children=
                [
                    dbc.Tab(label="UMAP", tab_id="UMAP"),
                    dbc.Tab(label="Violin Plot", tab_id= "Violin Plot"),
                ]
            ),
            dbc.Row([
                dbc.Col([html.Div(className="graph 1", children = [dcc.Graph(
                id='displayed_expression_umap'
            ),
                html.Div(download_modal(0), id='expression_download'),
            ]),], width=6),
                dbc.Col([
            html.Div(className="graph 2", children = [dcc.Graph(
                id='displayed_cell_type_umap'
            ),
                html.Div(download_modal(1), id='cell_type_download'),
            ])
                ], width=6)
            ]),       
            

            
        ]), width =10)
    ])
])

@callback(
    Output('displayed_expression_umap', 'figure'),
    Input('chosen_model', 'active_tab'),
    State("chosen_dataset","options"),
    Input('chosen_dataset', 'value'),
    Input('chosen_gene', 'value'),)
def update_displayed_exp_plot(model_value, opt, dataset_value, gene_value):
    """
    model_value: a string. One of: UMAP or violin plot
    opt: a dictionary storing dataset names as keys and the dataset reference as values
    dataset_value: a string. The dataset to use. Default: bbknn_point
    gene_value: a string. The gene_id to pass to the query. Default: Thoc1

    Returns a plotly figure
    """
    df = make_query(
        type="umap", 
        integration_method=dataset_value,
        gene_value=gene_value)

    gene_df = make_query(
        type="gene",  
        integration_method=dataset_value,
        gene_value=gene_value)

    if gene_df.empty:
        finaldf = df.copy(deep=False)
        finaldf['normalized_count'] = 0.0
    else:
        finaldf = pd.merge(df, gene_df, on='cell_id', how="left")
        finaldf['normalized_count'] = finaldf['normalized_count'].fillna(0)

    opacity = []
    for row in range(1000):
        if finaldf.loc[df.index[row], 'normalized_count'] == 0:
            opacity.append(0.1)
        else:
            opacity.append(1)

    if model_value == 'UMAP':
        fig = px.scatter(
            finaldf, 
            x= "umap_1", 
            y= "umap_2", 
            labels={
                "umap_1": 'UMAP_1',
                "umap_2": 'UMAP_2',
                "normalized_count": "Log-Normalized <br>Expression",
            },
            color='normalized_count',
            opacity= opacity,
            height=400)

        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black', 
            mirror=True, 
            ticks="outside")

        fig.update_yaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',
            mirror=True, 
            ticks="outside")   

    elif model_value == 'Violin Plot':
        fig = px.violin(
            finaldf,
            y= 'normalized_count',
            labels = {
                "normalized_count": "Expression Level"
            },
            title=f'{gene_value}',
            points=False,)
        
        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',  
            ticks="outside",
            tickangle= -45)

        fig.update_yaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',
            ticks="outside",
            range= [0, 4])   

    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size= 10,
        plot_bgcolor='rgb(255,255,255)',
        title = {
            'text': f'<b>{gene_value}</b>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size': 20
        },
        legend_title = "Cell Types"
    )

    fig.update_traces(
        hovertemplate=None,
        hoverinfo='skip'
    )

    return fig

@callback(
    Output('displayed_cell_type_umap', 'figure'),
    Input('chosen_model', 'active_tab'),
    Input('chosen_dataset', 'value'),
    Input('chosen_gene', 'value'),
    State("chosen_dataset","options"))
def update_displayed_ctype_plot(model_value, dataset_value, gene_value, opt):
    """
    model_value: a string. One of: UMAP or violin plot
    opt: a dictionary storing dataset names as keys and the dataset reference as values
    dataset_value: a string. The dataset to use. Default: bbknn_point
    gene_value: a string. The gene_id to pass to the query. Default: Thoc1

    Returns a plotly figure
    """
    cell_type_df = make_query(
        type="umap", 
        integration_method=dataset_value,
        gene_value=gene_value)

    gene_df = make_query(
        type="gene",  
        integration_method=dataset_value,
        gene_value=gene_value)

    if gene_df.empty:
        finaldf = cell_type_df.copy(deep=False)
        finaldf['normalized_count'] = 0.0
    else:
        finaldf = pd.merge(cell_type_df, gene_df, on='cell_id', how="left")
        finaldf['normalized_count'] = finaldf['normalized_count'].fillna(0)

    fig = go.Figure()
    if model_value == "UMAP":
        fig = px.scatter(
            finaldf, 
            x='umap_1', 
            y='umap_2', 
            hover_name='cell_id',
            title=f'{gene_value}',
            labels={
                "umap_1": 'UMAP_1',
                "umap_2": 'UMAP_2',
            },
            color= "cell_type",
            size_max=10,
            height=400)

        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black', 
            mirror=True, 
            ticks="outside")

        fig.update_yaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',
            mirror=True, 
            ticks="outside") 

        fig.update_layout(
            font_color=colors['text'],
            font_family='sans-serif',
            font_size=10,
            plot_bgcolor='rgb(255,255,255)',
            title={
                'text': f'<b>{gene_value}</b>',
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font_size': 20
            },
            legend_title="Cell Types",
            legend=dict(font=(dict(size=10)))
        )


        fig.update_traces(
            hovertemplate=None,
            hoverinfo='skip'
        )
    elif model_value == "Violin Plot": 
        fig = px.violin(
            finaldf, 
            x= 'cell_type',
            y= 'normalized_count',
            labels = {
                "cell_type": "Cell Type",
                "normalized_count": "Expression Level"
            },
            title=f'{gene_value}',
            points=False,
            color= 'cell_type')
        
        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',  
            ticks="outside",
            tickangle= -45)

        fig.update_yaxes(
            showline=True, 
            linewidth=1, 
            linecolor='black',
            ticks="outside",
            range= [0, 4])
    
    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size= 10,
        plot_bgcolor='rgb(255,255,255)',
        title = {
            'text': f'<b>{gene_value}</b>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size': 20
        },
        legend_title = "Cell Types"
    )

    fig.update_traces(
        hovertemplate=None,
        hoverinfo='skip'
    )

    return fig

### DOWNLOAD HANDLER 1 ###
@callback(
    Output("modal_0", "is_open"),
    [Input("open_0", "n_clicks")],
    [State("modal_0", "is_open")],
)
def toggle_modal(n1, is_open):
    """
    n1: a Dash Input, if the button was clicked 
    is_open: a Dash State, whether or not the modal is open

    returns the state of the modal - open or closed
    """
    if n1:
        return not is_open
    return is_open

@callback(
    Output("download-output_0", "children"),
    Input("displayed_expression_umap", "figure"),
    Input("file-name_0", "value"),
    Input("chosen_download_option_0", "value"),
    Input("horizontal_0", "value"),
    Input("vertical_0", "value"),
    Input("download_0", "n_clicks"),
    prevent_initial_call=True,
)
def download_exp_handler(fig, name, file_ext, width, height, click):
    if click:
        fig = go.Figure(fig)

        # converts inches to pixels
        width= int(width)*96
        height=int(height)*96

        fig.write_image(f'./images/{name}.{file_ext}', width=width, height=height)

### DOWNLOAD HANDLER 2 ###
@callback(
    Output("modal_1", "is_open"),
    [Input("open_1", "n_clicks")],
    [State("modal_1", "is_open")],
)
def toggle_modal_2(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("download-output_1", "children"),
    Input("displayed_cell_type_umap", "figure"),
    Input("file-name_1", "value"),
    Input("chosen_download_option_1", "value"),
    Input("horizontal_1", "value"),
    Input("vertical_1", "value"),
    Input("download_1", "n_clicks"),
    prevent_initial_call=True,
)
def download_cell_type_handler(fig, name, file_ext, width, height, click):
    if click:
        fig = go.Figure(fig)

        # converts inches to pixels
        width= int(width)*96
        height=int(height)*96

        fig.write_image(f'./images/{name}.{file_ext}', width=width, height=height)