"""
Navbar for Web App
"""

import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("scRNA", href="/")),
            dbc.NavItem(dbc.NavLink("Histology", href="/histology")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Pediatric Skeletal Muscle Cell Atlas",
        brand_href="/",
        color="white",
        dark=False,
    )