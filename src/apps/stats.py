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

df=pd.read_csv("../data/processed/airbnb_data.csv")

# ---------------------app components-------------------
# Violin plot
alt.data_transformers.enable('default', max_rows=None)
# def plot_altair(min_one, max_one):
#     violin=alt.Chart(df[(df.rating >= min_one) & (df.rating <= max_one) ]).transform_density("price",as_=["price","density"],extent=[0, 1000],groupby=["room_type"]).mark_area(orient='horizontal').encode(
#         alt.X('density:Q')
#             .stack('center')
#             .impute(None)
#             .title(None)
#             .axis(labels=False, values=[0], grid=False, ticks=True),
#         alt.Y('price:Q'),
#         alt.Color('room_type:N'),
#         alt.Column('room_type:N')
#             .spacing(0)
#             .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
#     ).configure_view(
#         stroke=None
#     )
#     return violin.to_html()



rating=dbc.Card([
    dbc.CardHeader("Plases select rating range",
                   style={'font-size':'18px',
                          'font-family':'Cascadia Code',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody([
        dcc.RangeSlider(id='rating',
                        min=df['rating'].min(),
                        max=df['rating'].max())
    ])
])

number_rate=dbc.Card([
    dbc.CardBody([
        html.Iframe(id='number_rating', style={'border-width': '0', 'width': '100%', 'height': '580px'})
        ])
    ])


# ---------------------layout-------------------
layout=dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this map tab"),
        html.Hr(),
        #badge,
        dbc.Row([
            number_rate
            # html.Iframe(
            #     id='violin',
            #     srcDoc=plot_altair(min_one=df.rating.min(),max_one=df.rating.max()),
            #     style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ,rating
            # dbc.Col([
            #         rating
            #     ])
            # ,dbc.Col(number_rate)
        ],
        justify='end')
    ],
    style=CONTENT_STYLE,
    fluid=True
)
# ---------------------call back-------------------   
# Callback
@callback(
    Output('number_rating', 'srcDoc'),
    Input('rating', 'value')
)
def update_bar_chart(choice):
    min_value, max_value = choice
    number_rating = alt.Chart(df[(df.rating >= min_value) & (df.rating <= max_value)]).transform_density(
        "price", as_=["price", "density"], extent=[0, 1000], groupby=["room_type"]).mark_area(
        orient='horizontal').encode(
        alt.X('density:Q')
            .stack('center')
            .impute(None)
            .title(None)
            .axis(labels=False, values=[0], grid=False, ticks=True),
        alt.Y('price:Q'),
        alt.Color('room_type:N'),
        alt.Column('room_type:N')
            .spacing(0)
            .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
    ).configure_view(
        stroke=None
    )
    return number_rating.to_html()
# def update_output(choice):
#     min_value, max_value = choice
#     return plot_altair(min_one=min_value, max_one=max_value)