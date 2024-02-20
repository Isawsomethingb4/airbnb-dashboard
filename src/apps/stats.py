import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
dash.register_page(__name__, path='/statistics')

# Import dataset

airbnb_data = pd.read_csv("../data/processed/airbnb_data.csv")

# Content Style

CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Layout

layout = dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this statistics tab"),
        html.Hr()
    ],
    style=CONTENT_STYLE,
    fluid=True
)