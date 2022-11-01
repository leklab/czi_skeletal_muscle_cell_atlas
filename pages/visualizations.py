import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from scripts.query import make_query
from components.download import download_modal
from components.options import visualization_options

colors = {
    'text': '#000000'
}

dash.register_page(__name__, path="/")

layout = html.Div([
    dbc.Row([
        dbc.Col(visualization_options() , width=2),
        dbc.Col(html.Div(className="visualizations", children=[
            dbc.Tabs(id="chosen_model", active_tab="UMAP", children=[
                dbc.Tab(label="UMAP", tab_id="UMAP"),
                dbc.Tab(label="Violin Plot", tab_id="Violin Plot"),
                dbc.Tab(label="Dot Plot", tab_id="Dot Plot")
            ]
            ),
            dbc.Row([
                dbc.Col([html.Div(className="graph 1", children=[dcc.Graph(
                    id='displayed_expression_umap'
                ),
                    html.Div(download_modal(0), id='expression_download'),
                ]), ], width=6),
                dbc.Col([
                    html.Div(className="graph 2", children=[dcc.Graph(
                        id='displayed_cell_type_umap'
                    ),
                        html.Div(download_modal(1), id='cell_type_download'),
                    ])
                ], width=6)
            ]),

        ]), width=10)
    ])
], style={'margin-left': '5%', 'margin-right': '5%'})


@callback(
    Output('displayed_expression_umap', 'figure'),
    Input('chosen_model', 'active_tab'),
    State("chosen_dataset", "options"),
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

    fig = go.Figure()
    if model_value == 'UMAP':
        try:
            fig = px.scatter(
                finaldf,
                x="umap_1",
                y="umap_2",
                labels={
                    "umap_1": 'UMAP_1',
                    "umap_2": 'UMAP_2',
                    "normalized_count": "Log-Normalized <br>Expression",
                },
                color='normalized_count',
                opacity=opacity)
        except:
            fig = px.scatter(
                finaldf,
                x="umap_1",
                y="umap_2",
                labels={
                    "umap_1": 'UMAP_1',
                    "umap_2": 'UMAP_2',
                    "normalized_count": "Log-Normalized <br>Expression",
                },
                color='normalized_count',
                opacity=opacity,
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
            y='normalized_count',
            labels={
                "normalized_count": "Expression Level"
            },
            title=f'{gene_value}',
            points=False,)

        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks="outside",
            tickangle=-45)

        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks="outside",
            range=[0, 4])

    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        title={
            'text': f'<em>{gene_value}</em>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size': 20
        },
        legend_title="Cell Types",
        height=375,
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
    State("chosen_dataset", "options"))
def update_displayed_ctype_plot(model_value, dataset_value, gene_value, opt):
    """
    model_value: a string. One of: UMAP or violin plot
    opt: a dictionary storing dataset names as keys and the dataset reference as values
    dataset_value: a string. The dataset to use. Default: bbknn_point
    gene_value: a string. The gene_id to pass to the query. Default: Thoc1

    Returns a plotly figure
    """
    text_colors = ["#F6222E", "#FE00FA", "#16FF32", "#3283FE", "#FEAF16",
                   "#B00068", "#1CFFCE", "#1C8356", "#2ED9FF", "#DEA0FD", "#AA0DFE",
                   "#1CBE4F", "#F8A19F", "#325A9B", "#C4451C", "#1C7F93", "#85660D",
                   "#B10DA1", "#FBE426", "#BDCDFF", "#90AD1C", "#B5EFB5", "#822E1C",
                   "#7ED7D1", "#D85FF7", "#683B79"]  # "#66B0FF", "#3B00FB", "#FA0087", "#FC1CBF", "#F7E1A0", "#C075A6", "#782AB6", "#AAF400"]

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
        try:
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
                color="cell_type",
                color_discrete_sequence=text_colors,
                size_max=10,
                height=400)
        except:
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
                color="cell_type",
                color_discrete_sequence=text_colors,
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
            legend=dict(font=(dict(size=10))),
            autosize=False,
            height=400
        )

        fig.update_traces(
            hovertemplate=None,
            hoverinfo='skip'
        )
    elif model_value == "Violin Plot":
        fig = px.violin(
            finaldf,
            x='cell_type',
            y='normalized_count',
            labels={
                "cell_type": "Cell Type",
                "normalized_count": "Expression Level"
            },
            title=f'{gene_value}',
            points=False,
            color='cell_type')

        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks="outside",
            tickangle=-45)

        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks="outside",
            range=[0, 4])

    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        title={
            'text': f'<em>{gene_value}</em>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size': 20
        },
        legend_title="Cell Types",
        autosize=False,
        height=400,
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
        width = int(width)*96
        height = int(height)*96

        fig.write_image(f'./images/{name}.{file_ext}',
                        width=width, height=height)

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
        width = int(width)*96
        height = int(height)*96

        fig.write_image(f'./images/{name}.{file_ext}',
                        width=width, height=height)
