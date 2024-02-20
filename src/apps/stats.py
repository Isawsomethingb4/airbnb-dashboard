import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
dash.register_page(__name__, path='/statistics')

# ---------------------content style-------------------
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# ---------------------import data-------------------

listings=pd.read_csv("../data/processed/airbnb_data.csv")

# ---------------------app components-------------------

rating=dbc.Card([
    dbc.CardHeader("Plases select rating range",
                   style={'font-size':'18px',
                          'font-family':'Cascadia Code',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody([
        dcc.RangeSlider(id='rating',
                        min=listings['rating'].min(),
                        max=listings['rating'].max())
    ])
])
# number_rate=dbc.Card([
#     dbc.CardBody([
#         html.Iframe(id='rating_bar', style={'border-width': '0', 'width': '100%', 'height': '580px'})
#         ])
#     ])
# ---------------------layout-------------------
layout=dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this map tab"),
        html.Hr(),
        #badge,
        dbc.Row([
            dbc.Col([
                    rating
                ])
            # ,dbc.Col(number_rate)
        ],
        justify='end')
    ],
    style=CONTENT_STYLE,
    fluid=True
)