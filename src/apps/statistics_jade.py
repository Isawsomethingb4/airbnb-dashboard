import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
dash.register_page(__name__, path='/statistics')


# # ---------------------import data-------------------

# listings=pd.read_csv("../data/processed/airbnb_data.csv")
# CITY=listings['city'].unique().tolist()

# # ---------------------content style-------------------
# CONTENT_STYLE = {
#     "margin-left": "24rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
# }

# # ---------------------app components-------------------
# # badge = dbc.Button(
# #     [
# #         "Notifications",
# #         dbc.Badge("4", color="light", text_color="primary", className="ms-1"),
# #     ],
# #     color="primary",
# # )
# button=dbc.Button("Location", color="primary", className="btn btn-primary btn-lg")
# location=dbc.Card(
#     [
#         html.Div([
#                 dbc.Label("City"),# label to display
#                 dcc.Dropdown(
#                     id='city',
#                     options=[
#                         {'label': city, 'value': city} for city in CITY
#                     ],
#                     value='Vancouver'
#                 )
#             ]),

#         html.Div([
#             dbc.Label('Neighbourhood'),
#             dcc.Dropdown(
#                 id='neighbourhood',
#                 value='Downtown'
#             )

#         ])

#     ],
#     body=True
# )
# price=dbc.Card([
#     dbc.CardHeader("Plases select price range",
#                    style={'font-size':'18px',
#                           'font-family':'Cascadia Code',
#                           'background':'rgba(0,0,0,0)'}),
#     dbc.CardBody([
#         dcc.RangeSlider(id='price',
#                         min=listings['price'].min(),
#                         max=listings['price'].max())
#     ])
# ])
# number=dbc.Card([
#     dbc.CardBody([
#         html.Iframe(id='number_bar', style={'border-width': '0', 'width': '100%', 'height': '580px'})
#         ])
#     ])




# # ---------------------layout-------------------
# layout=dbc.Container(
#     children=[
#         html.H1("Welcome to Airbnb Dashboard"),
#         html.P("This is some introductory text about this map tab"),
#         html.Hr(),
#         #badge,
#         dbc.Row([
#             dbc.Col([
#                     button,
#                     location,
#                     price
#                 ]),
#             dbc.Col(number)
#         ],
#         justify='end')
#     ],
#     style=CONTENT_STYLE,
#     fluid=True
# )
layout=dbc.Container(
    children=[
        html.H1("welcome")
    ]
)

# # ---------------------call back-------------------   
# # decide neighbourhood with city
# @callback(
#     Output('neighbourhood', 'options'),
#     [Input('city', 'value')]
# )
# def update_neighbourhood(city):
#     neighbourhoods=listings.loc[listings['city']==city, 'neighbourhood'].unique().tolist()
#     options=[{'label': neighbourhood, 'value': neighbourhood} for neighbourhood in neighbourhoods]
#     return options

# #decide number of listing bar plot with city
# @callback(
#     Output('number_bar', 'srcDoc'),
#     [Input('city', 'value')]
# )
# def update_bar_chart(city):
#     number=listings.groupby(['city', 'neighbourhood'])['id'].count()
#     city_df=number.loc[city, ].reset_index().rename(columns={'id':'count'})
#     number_bar=alt.Chart(city_df, title=f'Number of Listings in {city}').mark_bar().encode(
#     x=alt.X('count', title='Total Number'),
#     y=alt.Y('neighbourhood', sort='x', title='Neighbourhood'),
#     tooltip='count'
#     )#.interactive()
#     return number_bar.to_html()
    



