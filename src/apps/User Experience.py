import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
dash.register_page(__name__, path='/experience')

airbnb_data = pd.read_csv("data/processed/airbnb_data.csv")
airbnb_data.dropna(subset=["price"],inplace=True)
airbnb_data=airbnb_data.query("minimum_nights > 90 and rating<5")
airbnb_data.rename(columns={"rating":"Rating","minimum_nights":"MinimumNights","number_of_reviews":"Reviews"},inplace=True)
def round_to_hundreds(x):
    return np.ceil(x / 100) * 100
airbnb_data["Reviews"] = airbnb_data["Reviews"].apply(round_to_hundreds)

alt.data_transformers.enable('default', max_rows=None)

# Content Style
CONTENT_STYLE = {
    "margin-left": "0%",
    "margin-right": "0%",
    "padding": "2rem 1rem",
}

# App Components


# Layout
layout = dbc.Container(
    [
        html.H3('5. Minimum Night vs Average Price'),
        html.Div([
            'This is my dropdown',
            dcc.Dropdown(id="features",
                options=[
                    {'label': 'Rating', 'value': 'Rating'},
                    {'label': 'Reviews', 'value': 'Reviews'},
                {'label': 'Minimum Nights', 'value': 'Minimum Nights'}],
                value='Minimum Nights')]),
        # dvc.Vega(
        #     id="x_axis",
        #     opt={"renderer": "svg", "actions": False})
            # spec=chart.to_dict())
        # html.Div([
            html.Iframe(id='x_axis', width='1250', height='1000')
        # ]),
    ],
    style=CONTENT_STYLE,
    fluid=True
)


# ---------------------call back-------------------
@callback(
        Output('x_axis', 'srcDoc'),
        [Input('features', 'value')]
)
def update_plots(x_label):
    # if x_label is None:
    #     x_label = "MinimumNights"
    click = alt.selection_multi(fields=['city'], bind='legend')
    brush = alt.selection_interval()
    int1 = alt.Chart(airbnb_data).mark_rect().encode(
        x=alt.X("room_type", title="Room Type", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        y=alt.Y("city", title="City", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        color=alt.condition(
            brush,
            'count()',
            alt.value('lightgray'))
    ).properties(
        width=180,
        height=180
    ).add_selection(
        brush
    )

    int2 = alt.Chart(airbnb_data).mark_point(filled=False, clip=True).encode(
        y=alt.Y("mean(price)", title="Average Price", scale=alt.Scale(domain=[0, 600]),
                axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        x=alt.X(x_label, type="quantitative",scale=alt.Scale(zero=False),
                # title="Minimum Night", scale=alt.Scale(domain=[0, 90], zero=False),
                axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        color=alt.condition(
            brush,
            'room_type',
            alt.value('lightgray')
        ),
        tooltip=["mean(Rating)", "city"]
    ).add_selection(
        brush
    )

    bars = (alt.Chart(airbnb_data).mark_bar().encode(
        x=alt.X('count()', title="Count", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        y=alt.Y('city', title="City", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))
            .transform_filter(brush))

    chart = (int1.properties(height=450, width=350) | (int2 & bars)).add_selection(
        click
    )
    return chart.to_html()



