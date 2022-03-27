import pandas as pd

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

import pydeck as pdk
import dash_deck

mapbox_api_token = "pk.eyJ1Ijoia2FyYW4tcy1taXR0YWwiLCJhIjoiY2s4bHRhb3RlMDUyMjNubjh5N3R1dmNydSJ9.e6Y_UslQeahIikTwsRny3w"

dash.register_page(
    __name__,
    path="/co2-layer",
    title="Co2 Layer",
)

main_df = pd.read_csv(
    "https://media.githubusercontent.com/media/Karan-S-Mittal/Peter-Re-Cash/main/data/re_cash_columns.csv"
)

print(main_df.info())

gde_name_list = main_df["GDENAME"].unique()
# Main
layout = dbc.Row(
    [
        # Controls
        dbc.Col(
            [
                html.H4("Select Area"),
                dcc.Dropdown(
                    id="map-controls-gde",
                    options=gde_name_list,
                    value=gde_name_list[0],
                    multi=True,
                ),
            ],
            width=2,
        ),
        # Maps
        dbc.Col(
            [
                html.Div(
                    [],
                    id="map-graph",
                    style={
                        "height": "600px",
                        "width": "100%",
                        "position": "relative",
                    },
                ),
            ],
            width=10,
        ),
    ],
)


@callback(Output("map-graph", "children"), Input("map-controls-gde", "value"))
def update_map(gde_list):

    TOOLTIP_TEXT = {
        "html": "<b>Elevation Value:</b> {elevationValue}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
        },
    }
    if type(gde_list) == str:
        gde_list = [gde_list]
    print(gde_list)
    df = main_df[main_df["GDENAME"].isin(gde_list)]

    layer = pdk.Layer(
        "HexagonLayer",  # `type` positional argument is here
        df,
        get_position=["Longitude", "Latitude"],
        auto_highlight=True,
        elevation_scale=20,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1,
    )

    view_state = pdk.ViewState(
        longitude=8.1355,
        latitude=46.7,
        zoom=7,
        min_zoom=6,
        max_zoom=15,
        pitch=40.5,
        bearing=-20.36,
    )

    # Combined all of it and render a viewport
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=TOOLTIP_TEXT,
        api_keys={"mapbox": mapbox_api_token},  # new line
        map_provider="mapbox",
        map_style=pdk.map_styles.ROAD,  # new line
    )
    # r.to_html("some-file.html")

    result = dash_deck.DeckGL(
        r.to_json(),
        id="co2_layer",
        tooltip=TOOLTIP_TEXT,
        mapboxKey=r.mapbox_key,  # new line
        # style={"width": "55vw", "height": "75vh"},
    )
    return result
