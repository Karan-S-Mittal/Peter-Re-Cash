import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

import pages_plugin

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
]

external_scripts = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js",
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    suppress_callback_exceptions=True,
    plugins=[
        pages_plugin,
    ],
)

server = app.server

# Basic UI elements

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url("images/pom-logo.png"),
                                height="30px",
                            )
                        ),
                        dbc.Col(dbc.NavbarBrand("Peter", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                [
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem(page["name"], href=page["path"])
                            for page in dash.page_registry.values()
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Graphs & Visualisations",
                        color="dark",
                        style={"color": "white"},
                    ),
                ],
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="secondary",
    dark=True,
)


app.layout = html.Div(
    [
        # header section
        navbar,
        # Set the container where the page content will be rendered into on page navigation
        html.Main(pages_plugin.page_container, className="row"),
        # footer section
    ],
    className="container-fluid",
)

if __name__ == "__main__":
    app.run_server(debug=True)
