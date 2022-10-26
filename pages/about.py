import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

### RESOURCE ###
# Template format for html <a> tags, define and use variables accordingly
# link1 = html.A('TITLE', href="")

github = html.A('github', href="https://github.com/leklab/czi_skeletal_muscle_cell_atlas", target="_blank")

layout = html.Div([
    html.H5("About Pediatric Skeletal Cell Muscle Atlas"),
    html.P([
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eget nibh et purus condimentum blandit eget a odio. In elementum aliquam accumsan. Fusce semper libero id arcu varius rhoncus. Donec sed efficitur quam, et gravida nulla. Nam et elit nisl. Donec scelerisque iaculis auctor. Nulla cursus lectus at augue accumsan, id finibus tellus ultricies. Donec ullamcorper sollicitudin semper. Vivamus ac diam id felis porttitor tempus ",
        github,
        ". Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eget nibh et purus condimentum blandit eget a odio. In elementum aliquam accumsan. Fusce semper libero id arcu varius rhoncus. Donec sed efficitur quam, et gravida nulla. Nam et elit nisl. Donec scelerisque iaculis auctor. Nulla cursus lectus at augue accumsan, id finibus tellus ultricies. Donec ullamcorper sollicitudin semper. Vivamus ac diam id felis porttitor tempus."
        ]),
    html.H5("Web Development"),
    html.P([
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eget nibh et purus condimentum blandit eget a odio. In elementum aliquam accumsan. Fusce semper libero id arcu varius rhoncus. Donec sed efficitur quam, et gravida nulla. Nam et elit nisl. Donec scelerisque iaculis auctor. Nulla cursus lectus at augue accumsan, id finibus tellus ultricies. Donec ullamcorper sollicitudin semper. Vivamus ac diam id felis porttitor tempus."
        ]),
    html.H5("More Headings"),
    html.P([
        "More text"
        ])
],style={'margin-left': '5%', 'margin-right': '5%'})