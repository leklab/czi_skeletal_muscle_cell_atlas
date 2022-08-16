import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Visualizations", href="/")),
            dbc.NavItem(dbc.NavLink("Metadata", href="/metadata")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Pediatric Skeletal Muscle Cell Atlas",
        brand_href="/",
        color="white",
        dark=False,
    )