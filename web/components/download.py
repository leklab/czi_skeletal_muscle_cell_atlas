import dash_bootstrap_components as dbc
from dash import html, dcc

file_extensions = ["pdf", "svg", "png"]

def download_modal(number):
    return [
        dbc.Button("Download", id=f'open_{number}', n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Download Specifications")),
            dbc.ModalBody([
                html.Label(['File Name']),
                html.Div(className="download-file-name", children=
                    dcc.Input(
                        id=f"file-name_{number}",
                        value="My Figure",
                    )
                ),
                html.Label(['File Extension']),
                html.Div(className="download-file-extension", children=
                    dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in file_extensions
                        ],
                        value= "pdf",
                        id= f"chosen_download_option_{number}"
                    )
                ),
                html.Label(['Horizontal Dimensions (in)']),
                html.Div(className="dimensions", children=
                    dcc.Input(
                        id=f"horizontal_{number}",
                        value=10,
                        type="number"
                    )
                ),
                html.Label(['Vertical Dimensions (in)']),
                html.Div(className="dimensions", children=
                    dcc.Input(
                        id=f"vertical_{number}",
                        value=5,
                        type="number"
                    )
                )
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Download", 
                    id=f"download_{number}", 
                    className="ms-auto", 
                    n_clicks=0
                )
            ),
        ], id=f"modal_{number}", centered=True, is_open=False),
        html.Div(id=f"download-output_{number}")
    ]

# def downloadHandler(app, number):
#     @app.callback(
#     Output(f"modal_{number}", "is_open"),
#     [Input(f"open_{number}", "n_clicks")],
#     [State(f"modal_{number}", "is_open")],
# )
#     def toggle_modal(n1, is_open):
#         """
#         n1: a Dash Input, if the button was clicked 
#         is_open: a Dash State, whether or not the modal is open

#         returns the state of the modal - open or closed
#         """
#         if n1:
#             return not is_open
#         return is_open

#     @app.callback(
#         Output(f"download-output_{number}", "children"),
#         Input(f"displayed_expression_umap", "figure"), ### NEED TO CHANGE TO CELL TYPE
#         Input(f"file-name_{number}", "value"),
#         Input(f"chosen_download_option_{number}", "value"),
#         Input(f"horizontal_{number}", "value"),
#         Input(f"vertical_{number}", "value"),
#         Input(f"download_{number}", "n_clicks"),
#         prevent_initial_call=True,
#     )
#     def download_exp_handler(fig, name, file_ext, width, height, click):
#         if click:
#             fig = go.Figure(fig)

#             # converts inches to pixels
#             width= int(width)*96
#             height=int(height)*96

#             fig.write_image(f'./images/{name}.{file_ext}', width=width, height=height)
