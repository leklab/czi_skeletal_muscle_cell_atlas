import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import numpy as np

from scripts.query import make_query
from components.download import download_modal
from components.options import visualization_options

dash.register_page(__name__, path="/")

cell_type_order = [
    "MuSCs",
    "Endothelial (Artery)",
    "Endothelial (Vein)",
    "Endothelial (Capillary)",
    "Monocyte (Cxcl10+)",
    "Monocyte (Inflammatory)",
    "Monocyte (Patrolling)",
    "FAPs (Pro-remodeling)",
    "FAPs (Stem)",
    "FAPs (Adipogenic)",
    "Myonuclei (Type IIx)",
    "Myonuclei (Type IIb)",
    "M2 Macro. (Cx3cr1_hi)",
    "M2 Macro. (Cx3cr1_lo)",
    "T Cells",
    "B Cells",
    "Tenocytes",
    "Dendritic",
    "Smooth Muscle & Pericytes",
    "Myoblasts/Progenitors",
    "Neutrophils",
    "NK Cells",
    "Neural",
]

text_colors = ["#F6222E", "#FE00FA", "#16FF32", "#3283FE", "#FEAF16",
               "#B00068", "#1CFFCE", "#1C8356", "#2ED9FF", "#DEA0FD",
               "#AA0DFE", "#1CBE4F", "#F8A19F", "#325A9B", "#C4451C",
               "#1C7F93", "#85660D", "#B10DA1", "#FBE426", "#BDCDFF",
               "#90AD1C", "#B5EFB5", "#822E1C", "#7ED7D1", "#D85FF7",
               "#683B79"]

colors = {'text': '#000000'}

layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div(className="visualizations", children=[
            dbc.Tabs(id="chosen_model", active_tab="UMAP", children=[
                dbc.Tab(label="UMAP", tab_id="UMAP"),
                dbc.Tab(label="Violin Plot", tab_id="Violin Plot"),
                dbc.Tab(label="Dot Plot", tab_id="Dot Plot")
            ]),
            visualization_options(),
            dbc.Row(id="tab_output"),
            html.Div(dcc.Graph(id="displayed_umap_plot_expr"), style={'display':'none'}),
            html.Div(dcc.Graph(id="displayed_umap_plot_ctype"), style={'display':'none'}),
            html.Div(dcc.Graph(id="displayed_violin_plot_expr"), style={'display':'none'}),
            html.Div(dcc.Graph(id="displayed_violin_plot_ctype"), style={'display':'none'}),
            html.Div(dcc.Graph(id="displayed_dot_plot"), style={'display':'none'}),
        ]), width=12)
    ]),
], style={'margin-left': '5%', 'margin-right': '5%'})


@callback(
    Output('displayed_umap_plot_expr', 'figure'),
    Input('chosen_gene', 'value')
)
def update_umap_plot_expr(gene_value):
    gene_value = gene_value[0].split("\"")[0]
    df = make_query(type="umap", integration_method="harmony",
                    gene_value=gene_value)
    gene_df = make_query(
        type="gene", integration_method="harmony", gene_value=gene_value)

    if gene_df.empty:
        finaldf = df.assign(normalized_count=0.0)
    else:
        finaldf = pd.merge(df, gene_df, on='cell_id', how="left").assign(
            normalized_count=lambda x: x['normalized_count'].fillna(0))

    finaldf.loc[finaldf['normalized_count'] == 0, 'normalized_count'] = np.nan

    opacity = [0.3 if finaldf.loc[df.index[row], 'normalized_count'] == 0 else 1 for row in range(1000)]

    fig = px.scatter(
        finaldf,
        x="umap_1",
        y="umap_2",
        labels={"umap_1": 'UMAP_1', "umap_2": 'UMAP_2',
                "normalized_count": "Log-Normalized <br>Expression"},
        color='normalized_count',
        opacity=opacity
    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', mirror=True, ticks="outside")
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='black', mirror=True, ticks="outside")

    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        title={'text': f'<em>{gene_value}</em>', 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top', 'font_size': 20},
    )

    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    return fig


@callback(
    Output('displayed_umap_plot_ctype', 'figure'),
    Input('chosen_gene', 'value')
)
def update_umap_plot_ctype(gene_value):
    gene_value = gene_value[0].split("\"")[0]

    cell_type_df = make_query(
        type="umap",
        integration_method="harmony",
        gene_value=gene_value
    )

    gene_df = make_query(
        type="gene",
        integration_method="harmony",
        gene_value=gene_value
    )

    if gene_df.empty:
        finaldf = cell_type_df.assign(normalized_count=0.0)
    else:
        finaldf = pd.merge(cell_type_df, gene_df, on='cell_id', how="left").assign(
            normalized_count=lambda x: x['normalized_count'].fillna(0))

    try:
        fig = px.scatter(
            finaldf,
            x='umap_1',
            y='umap_2',
            labels={
                "umap_1": 'UMAP_1',
                "umap_2": 'UMAP_2',
            },
            color="cell_type",
            color_discrete_sequence=text_colors,
            category_orders={"cell_type": cell_type_order}
        )
    except:
        fig = px.scatter(
            finaldf,
            x='umap_1',
            y='umap_2',
            labels={
                "umap_1": 'UMAP_1',
                "umap_2": 'UMAP_2',
            },
            color="cell_type",
            color_discrete_sequence=text_colors,
            category_orders={"cell_type": cell_type_order}
        )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks="outside"
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks="outside"
    )

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
    )

    fig.update_traces(
        hovertemplate=None,
        hoverinfo='skip'
    )

    return fig


@callback(
    Output('displayed_violin_plot_expr', 'figure'),
    Input('chosen_gene', 'value')
)
def update_violin_plot_expr(gene_value):
    gene_value = gene_value[0].split("\"")[0]

    cell_type_df = make_query(
        type="umap", integration_method="harmony", gene_value=gene_value)
    gene_df = make_query(
        type="gene", integration_method="harmony", gene_value=gene_value)

    if gene_df.empty:
        finaldf = cell_type_df.assign(normalized_count=0.0)
    else:
        finaldf = pd.merge(cell_type_df, gene_df, on='cell_id', how="left").assign(
            normalized_count=lambda x: x['normalized_count'].fillna(0))

    fig = px.violin(
        finaldf,
        y='normalized_count',
        title=f'{gene_value}',
        points=False,
        labels={"normalized_count": "Expression Level"},
    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', ticks="outside", tickangle=-45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", range=[
                     0, math.ceil(finaldf["normalized_count"].max())])

    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        title={'text': f'<em>{gene_value}</em>', 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top', 'font_size': 20},
        legend_title="Cell Types"
    )

    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    return fig


@callback(
    Output('displayed_violin_plot_ctype', 'figure'),
    Input('chosen_gene', 'value')
)
def update_violin_plot_ctype(gene_value):
    # Split the gene value to remove quotes
    gene_value = gene_value[0].split("\"")[0]

    # Query for cell types and gene expression data
    cell_type_df = make_query(
        type="umap", integration_method="harmony", gene_value=gene_value)
    gene_df = make_query(
        type="gene", integration_method="harmony", gene_value=gene_value)

    # Merge dataframes and fill NaN values with 0
    finaldf = pd.merge(cell_type_df, gene_df, on='cell_id', how="left")
    finaldf['normalized_count'] = finaldf['normalized_count'].fillna(0)

    # Create violin plot using plotly
    fig = px.violin(
        finaldf,
        x='cell_type',
        y='normalized_count',
        labels={"cell_type": "Cell Type",
                "normalized_count": "Expression Level"},
        title=f'{gene_value}',
        points=False,
        color='cell_type'
    )

    # Format axes and layout
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', ticks="outside", tickangle=-45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks="outside", range=[
                     0, math.ceil(finaldf["normalized_count"].max())])
    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        title={'text': f'<em>{gene_value}</em>', 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top', 'font_size': 20},
        legend_title="Cell Types"
    )

    # Disable hover
    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    return fig


@callback(
    Output('displayed_dot_plot', 'figure'),
    Input('chosen_gene', 'value')
)
def update_dot_plot(gene_list):
   # initialize empty data frame to store results
    results_df = pd.DataFrame(columns=["gene_name", "cell_type", "normalized_count", "non_zero_fraction"])

    # loop over all genes in gene_list
    for gene_value in gene_list:
        # extract the gene name from the input string
        gene_name = gene_value.split("\"")[0]

        # query the data for cell types and gene expression
        cell_type_df = make_query(
            type="umap",
            integration_method="harmony",
            gene_value=gene_name
        )

        gene_df = make_query(
            type="gene",
            integration_method="harmony",
            gene_value=gene_name
        )

        # add gene_name to cell_type_df
        cell_type_df['gene_name'] = gene_name

        # merge the dataframes and fill in missing values with 0
        finaldf = pd.merge(cell_type_df[['gene_name', 'cell_type', 'cell_id']], gene_df, on='cell_id', how="left")
        finaldf['normalized_count'] = finaldf['normalized_count'].fillna(0)

        # group the data by cell type and calculate the mean expression and fraction of non-zero values
        grouped = finaldf.groupby("cell_type").agg(
            mean_expression=("normalized_count", "mean"),
            non_zero_fraction=("normalized_count", lambda x: (x != 0).mean())
        ).reset_index()
        grouped["gene_name"] = gene_name

        # add results to the data frame
        results_df = results_df.append(grouped[["gene_name", "cell_type", "mean_expression", "non_zero_fraction"]])

    # create the plot
    try:
        fig = px.scatter(
            results_df,
            x="gene_name",
            y="cell_type",
            color='mean_expression',
            size="non_zero_fraction",
            labels={
                "cell_type": "Cell Type",
                "mean_expression": "Log-Normalized<br>Expression",
                "gene_name": "Gene(s)"
            },
            category_orders={"cell_type": cell_type_order},
        )
    except:
        fig = px.scatter(
            results_df,
            x="gene_name",
            y="cell_type",
            color='mean_expression',
            size="non_zero_fraction",
            labels={
                "cell_type": "Cell Type",
                "mean_expression": "Log-Normalized<br>Expression",
                "gene_name": "Gene(s)"
            },
            category_orders={"cell_type": cell_type_order},
        )

    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', mirror=True, ticks="outside")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black',
                     mirror=True, ticks="outside", gridcolor="black")
    fig.update_layout(
        font_color=colors['text'],
        font_family='sans-serif',
        font_size=10,
        plot_bgcolor='rgb(255,255,255)',
        height=600,
    )

    return fig


### DOWNLOAD HANDLER 0 ###
@callback(
    Output("modal_0", "is_open"),
    [Input("open_0", "n_clicks"),
     Input("download_0", "n_clicks")],
    [State("modal_0", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """
    n1: a Dash Input, if the button was clicked 
    is_open: a Dash State, whether or not the modal is open

    returns the state of the modal - open or closed
    """
    return not is_open if n1 or n2 else is_open


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

        fig.write_image(
            f'./images/{name}.{file_ext}',
            width=width,
            height=height
        )


### DOWNLOAD HANDLER 1 ###


@callback(
    Output("modal_1", "is_open"),
    [Input("open_1", "n_clicks"),
     Input("download_1", "n_clicks")],
    [State("modal_1", "is_open")],
)
def toggle_modal_2(n1, n2, is_open):
    return not is_open if n1 or n2 else is_open


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

        fig.write_image(
            f'./images/{name}.{file_ext}',
            width=width,
            height=height
        )

@callback(
    Output('tab_output', 'children'),
    [Input('chosen_model', 'active_tab'),
     Input('displayed_umap_plot_expr', 'figure'),
     Input('displayed_umap_plot_ctype', 'figure'),
     Input('displayed_violin_plot_expr', 'figure'),
     Input('displayed_violin_plot_ctype', 'figure'),
     Input('displayed_dot_plot', 'figure'),
     ]
)
def update_visualization(model, umap_expr, umap_ctype, violin_expr, violin_ctype, dot):
    if model == "UMAP":
        return dbc.Row([
            dbc.Col([
                html.Div(className="graph 1", children=[
                    dcc.Graph(figure=umap_expr),
                ])
            ], width=6),
            dbc.Col([
                html.Div(className="graph 2", children=[
                    dcc.Graph(figure=umap_ctype),
                ])
            ], width=6),
        ])
    elif model == "Violin Plot":
        return dbc.Row([
            dbc.Col([
                html.Div(className="graph 1", children=[
                    dcc.Graph(figure=violin_expr),
                ])
            ], width=6),
            dbc.Col([
                html.Div(className="graph 2", children=[
                    dcc.Graph(figure=violin_ctype),
                ])
            ], width=6),
        ])
    else:
        return html.Div([
            dcc.Graph(figure=dot)
        ])
    return {}