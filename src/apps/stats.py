import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
dash.register_page(__name__, path='/statistics')

# Import dataset

airbnb_data = pd.read_csv("../data/processed/airbnb_data.csv")
alt.data_transformers.enable('default', max_rows=None)
airbnb_data['rating'] = pd.to_numeric(airbnb_data['rating'])
roomtypes = airbnb_data['room_type'].unique().tolist()

# Content Style

CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# App Components

chk_roomtype = dbc.Checklist(
    id='chk-roomtype',
    options=[
        {'label': roomtype, 'value': roomtype} for roomtype in roomtypes
    ],
    inline=True,
    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
    value=roomtypes
)

slider_rating = dcc.RangeSlider(
    id='rating_silder',
    min=0,
    max=airbnb_data['rating'].max()
)
# Plots

# Layout

layout = dbc.Container(
    children=[
        html.H1('Welcome to Airbnb Dashboard'),
        html.P('This is some introductory text about this statistics tab'),
        html.Hr(),
        html.H3('1. Room Type vs Price Comparison'),
        html.Div([
            slider_rating
        ], style = {'width': '50%'}),
        html.Div([
            html.Iframe(id='vp', width='950', height='400')
        ]),
        html.H3('2. City vs Rating Comparison'),
        chk_roomtype,
        html.Div([
            html.Iframe(
                id='line-plot', width='900', height='600'
            )
        ])
    ],
    style=CONTENT_STYLE,
    fluid=True
)


# Callbacks

@callback(
    Output('line-plot', 'srcDoc'),
    [Input('chk-roomtype', 'value')]
)
def line_plot(value=roomtypes):
    data = airbnb_data[airbnb_data['room_type'].isin(value)]
    line_city_vs_price_base = alt.Chart(data).encode(
        y=alt.Y('mean(price)', title='Average Price', axis=alt.Axis(titleFontSize=15, labelFontSize=13, format='$s'), scale=alt.Scale(zero=False)),
        x=alt.X('city', title='City', axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13))
    )

    line_city_vs_price = line_city_vs_price_base.mark_point(size=10) + line_city_vs_price_base.mark_line().properties(
        width=700,
        height=450
    )
    
    return line_city_vs_price.to_html()

@callback(
    Output('chk-roomtype', 'value'),
    [Input('chk-roomtype', 'value')]
)
def validate_checklist(value):
    if value is None or len(value) == 0:
        return roomtypes
    else:
        return value
    
@callback(
    Output('vp', 'srcDoc'),
    [Input('rating_silder', 'value')]
)
def update_violin_plot(choice):
    if choice == None:
        min_value = airbnb_data.rating.min()
        max_value = airbnb_data.rating.max()
    else:
        min_value, max_value = choice
    rating_df = airbnb_data[(airbnb_data.rating >= min_value) & (airbnb_data.rating <= max_value)]

    vp = alt.Chart(rating_df).transform_density("price", as_=["price", "density"], extent=[0, 1000],
                                                groupby=["room_type"]).mark_area(
        orient='horizontal').encode(
        alt.X('density:Q', title='Room Type', axis=alt.Axis(titleFontSize=15, labelFontSize=13))
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
        alt.Y('price:Q', title='Price', axis=alt.Axis(titleFontSize=15, labelFontSize=13, format='$.3s')),
        alt.Color('room_type:N'),
        alt.Column('room_type:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0),
        tooltip="price"
    ).properties(
        height=300,
        width=175
    ).configure_view(
        stroke=None
    )
    return vp.to_html()