import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
# import altair_viewer
dash.register_page(__name__, path='/page-2')
# ---------------------content style-------------------

CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# ---------------------import data-------------------

df = pd.read_csv("../data/processed/airbnb_data.csv")

# ---------------------app components-------------------
# Scatter plot
alt.data_transformers.enable('default', max_rows=None)

# slider_review = dcc.RangeSlider(
#     id='reviews_silder',
#     min=0,
#     max=df['number_of_reviews'].max()
# )


slider_review =dbc.Card([
    dbc.CardHeader("Reviews Range 👀",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody(
    dcc.RangeSlider(
        id='reviews_silder',
        min=0,
        max=df['number_of_reviews'].max()
))],style={"height":"100px","width":"150%"})
# ---------------------layout-------------------
layout = dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this map tab"),
        html.Hr(),
        # badge,
        html.H3('1. Rating vs Average Price'),
        html.Div([
            slider_review
        ], style={'width': '30%'}),
        html.Div([
            html.Iframe(id='scatter', width='950', height='600')
        ]),

    ],
    style=CONTENT_STYLE,
    fluid=True
)


# ---------------------call back-------------------
# Callback
@callback(
    Output('scatter', 'srcDoc'),
    [Input('reviews_silder', 'value')]
)
def update_price_rate_scatter(reviews):
    if reviews == None:
        min_value = df.number_of_reviews.min()
        max_value = df.number_of_reviews.max()
    else:
        min_value, max_value = reviews
    df_new = df[(df.number_of_reviews >= min_value) & (df.number_of_reviews <= max_value)]
    scatter=alt.Chart(df_new).mark_point(filled=False,clip=True).encode(y=alt.Y("mean(price)",title="Average price",axis=alt.Axis(titleFontSize=15,labelFontSize=13),scale=alt.Scale(domain=[0,600])),x=alt.X("rating:Q",title="Rating",axis=alt.Axis(titleFontSize=15,labelFontSize=13),scale=alt.Scale(zero=False)), color=alt.Color("mean(number_of_reviews)",scale=alt.Scale(scheme='cividis',reverse=True)), tooltip = ["mean(price)", "rating", "mean(number_of_reviews)"]).properties(width=700,height=450)
    # , tooltip = ["mean(price)", "rating", "number_of_reviews"]
    #                                                                     , color=alt.Color("mean(number_of_reviews)",
    #                                                                                       scale=alt.Scale(
    #                                                                                           scheme='cividis',
    #                                                                                           reverse=True)
    return scatter.to_html()
