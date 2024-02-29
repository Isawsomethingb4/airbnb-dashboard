import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_vega_components as dvc
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
    "margin-left": "30rem",
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

slider_rating =dbc.Card([
    dbc.CardHeader("Rating Range ⭐",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody(
    dcc.RangeSlider(
    id='rating_silder',
    min=0,
    max=airbnb_data['rating'].max()
))],style={"height":"100px","width":"100%"})

slider_review = dbc.Card([
    dbc.CardHeader("Reviews Range 👀",
                   style={'font-size': '18px',
                          'background': 'rgba(0,0,0,0)'}),
    dbc.CardBody(
        dcc.RangeSlider(
            id='reviews_silder',
            min=0,
            max=airbnb_data['number_of_reviews'].max()
        ))], style={"height": "100px", "width": "150%"})

# Plots
click = alt.selection_point(fields=['city'], bind='legend')
brush = alt.selection_interval()
int1 = alt.Chart(airbnb_data
).mark_rect().encode(
  x="city",
  y="room_type",
  color=alt.condition(
    brush,
    'count()',
    alt.value('lightgray'))
  ).properties(
    width=180,
    height=180
).add_params(
  brush
)

int2 = alt.Chart(airbnb_data).mark_point(filled=False,clip=True).encode(y=alt.Y("mean(price)",scale=alt.Scale(domain=[0,600])),x=alt.X("minimum_nights:Q",scale=alt.Scale(domain=[0,90],zero=False)),
  color=alt.condition(
    brush, # condition
    'room_type',  # if True
    alt.value('lightgray') # if False
  ),tooltip=["mean(rating)","city"]).add_params(
  brush
)

bars = (alt.Chart(airbnb_data).mark_bar().encode(
    x='count()',
    y='city',
    # color='city',
    opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))
   .transform_filter(brush))

chart=int1.properties(height=450,width=400)| (int2 & bars).add_params(click)
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
        ]),
        html.H3('3. Rating vs Average Price'),
        html.Div([
            slider_review
        ], style={'width': '30%'}),
        html.Div([
            html.Iframe(id='scatter', width='1000', height='600')
        ]),
        html.H3('4. Minimum_night vs Average Price'),
        dvc.Vega(
            id="altair-chart",
            opt={"renderer": "svg", "actions": False},
            spec=chart.to_dict(),
        )

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
        alt.X('density:Q')
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
        alt.Y('price:Q', title='Price', axis=alt.Axis(titleFontSize=15, labelFontSize=13, format='$.3s')),
        alt.Color('room_type:N'),
        alt.Column('room_type:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0,titleFontSize=15,labelFontSize=13,title='Room Type'),
        tooltip="price"
    ).properties(
        height=300,
        width=175
    ).configure_view(
        stroke=None
    )
    return vp.to_html()


@callback(
    Output('scatter', 'srcDoc'),
    [Input('reviews_silder', 'value')]
)
def update_price_rate_scatter(reviews):
    if reviews == None:
        min_value = airbnb_data.number_of_reviews.min()
        max_value = airbnb_data.number_of_reviews.max()
    else:
        min_value, max_value = reviews
    df_new = airbnb_data[(airbnb_data.number_of_reviews >= min_value) & (airbnb_data.number_of_reviews <= max_value)]
    scatter = alt.Chart(df_new).mark_point(filled=False, clip=True).encode(
        y=alt.Y("mean(price)", title="Average price", axis=alt.Axis(titleFontSize=15, labelFontSize=13),
                scale=alt.Scale(domain=[0, 600])),
        x=alt.X("rating:Q", title="Rating", axis=alt.Axis(titleFontSize=15, labelFontSize=13),
                scale=alt.Scale(zero=False)),
        color=alt.Color("mean(number_of_reviews)", scale=alt.Scale(scheme='cividis', reverse=True)),
        tooltip=["mean(price)", "rating", "mean(number_of_reviews)"]).properties(width=700, height=450)
    return scatter.to_html()
