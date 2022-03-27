import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/home",
    title="Real Estate Report",
)

layout = html.H1("This is Home")
