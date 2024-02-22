import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt

dash.register_page(__name__, path='/statistics')

# ---------------------content style-------------------
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "20rem",
    "padding": "2rem 1rem",
}

# ---------------------import data-------------------

df = pd.read_csv("../data/processed/airbnb_data.csv")

# ---------------------app components-------------------
# Violin plot
alt.data_transformers.enable('default', max_rows=None)

violin = dbc.Card([
    dbc.CardBody([
        html.Iframe(id='vp', style={'width': '100%', 'height': '400px'})
    ])
])

rating = dbc.Card([
    dbc.CardHeader("Plases select rating range",
                   style={'font-size': '18px',
                          'font-family': 'Cascadia Code',
                          'background': 'rgba(0,0,0,0)'}),
    dbc.CardBody([
        html.Div(
        dcc.RangeSlider(id='rating_silder',
                        min=df['rating'].min(),
                        max=df['rating'].max()
                        ),
           style={'border-width': '0', 'width': '50%', 'height': '50px'}
        )])
])
# ---------------------layout-------------------
layout = dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this map tab"),
        html.Hr(),
        # badge,

        dbc.Row([
            violin,
            rating,
        ],justify='center')

    ],
    style=CONTENT_STYLE,
    fluid=True
)


# ---------------------call back-------------------
# Callback
@callback(
    Output('vp', 'srcDoc'),
    [Input('rating_silder', 'value')]
)
def update_violin_plot(choice):
    if choice == None:
        min_value = df.rating.min()
        max_value = df.rating.max()
    else:
        min_value, max_value = choice
    rating_df = df[(df.rating >= min_value) & (df.rating <= max_value)]

    vp = alt.Chart(rating_df).transform_density("price", as_=["price", "density"], extent=[0, 1000],
                                                groupby=["room_type"]).mark_area(
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
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0),
        tooltip="price"
    ).configure_view(
        stroke=None
    ).interactive()
    return vp.to_html()
