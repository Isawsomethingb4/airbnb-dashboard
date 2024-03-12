import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_vega_components as dvc
from dash import callback_context
import dash_bootstrap_components as dbc
from dash_table import DataTable
import pandas as pd
import numpy as np
import altair as alt
dash.register_page(__name__, path='/new')

airbnb_data =  pd.read_csv("../data/processed/airbnb_data.csv")
airbnb_data.dropna(subset=airbnb_data.columns.difference(['license']), inplace=True)
airbnb_data=airbnb_data.query("minimum_nights < 90 and rating<5 and rating>3.5")
airbnb_data.rename(columns={"host_name":"Host Name","rating":"Rating","minimum_nights":"Minimum Nights","number_of_reviews":"Reviews"},inplace=True)
def round_to_ten(x):
    return np.ceil(x / 20) * 20
airbnb_data["Reviews"]=airbnb_data["Reviews"].apply(round_to_ten)
def round_to_10(x):
    return np.ceil(x / 10) * 10
airbnb_data["price"]=airbnb_data["price"].apply(round_to_10)
def round_to_point1(x):
    return np.ceil(x / 0.02) * 0.02
airbnb_data["Minimum Nights"] = airbnb_data["Minimum Nights"].apply(round_to_point1)


airbnb_data["default_hosts"] = airbnb_data["Minimum Nights"]*airbnb_data["price"]
hosts_average = airbnb_data.sort_values(by=["default_hosts"])
hosts_average = hosts_average.iloc[0:3]
default_hosts = hosts_average[['Host Name', 'host url',"Minimum Nights","price"]]
# ---------------------content style-------------------
CONTENT_STYLE = {
    "margin-left": "0%",
    "margin-right": "0%",
    # "padding": "2rem 1rem",
    # 'height' : '100%',
    # "width": "90%",
    # "margin": "0 auto",
}

# Plot
alt.data_transformers.enable('default', max_rows=None)

# # App Components
# dropdown_choice = dbc.Card([
#     dbc.CardHeader("What do you concern?",
#                    style={'font-size':'18px',
#                           'background':'rgba(0,0,0,0)',
#                           'textAlign':'center'}),
#     dbc.CardBody([
#         dcc.Dropdown(id="features",
#                      options=[
#                          {'label': 'Rating', 'value': 'Rating'},
#                          {'label': 'Reviews', 'value': 'Reviews'},
#                          {'label': 'Minimum Nights', 'value': 'Minimum Nights'}],
#                      value='Minimum Nights'),
#         html.Br(),
#         html.H4(id="formular",
#                 style={
#                     'textAlign': 'center',
#                     'color': '#FF9874',
#                     'fontSize': 25
#                 }
#                 )
#     ])
# ],
#     className='card',
#     style={
#                     'width': '60%',
#                     'margin-left': '18%',
#                      'height': '100%'
#                 #     'margin':'auto',
#                  }
# )


# Layout
layout = dbc.Container(
    [
        # html.H1("User Concerns", style={"textAlign": "center"}),
        dbc.Stack([
            # html.Br(),
            html.H1("User Concerns", style={"textAlign": "center", 'color': '#FF9874', 'fontSize': 45,
                                            "textShadow": "2px 2px 2px #000000"})]),
        html.P("Explore Average Price based on important Features and make a best choice.",
               style={"textAlign": "center"}),
        # html.Hr(),
            dbc.CardBody([
                dcc.Dropdown(id="feature",
                             options=[
                                 {'label': 'Rating', 'value': 'Rating'},
                                 {'label': 'Reviews', 'value': 'Reviews'},
                                 {'label': 'Minimum Nights', 'value': 'Minimum Nights'}],
                             value='Minimum Nights') ]),
        #     dbc.Row([
        #         dbc.Col(hosts),
        #         dbc.Col(dropdown_choice)
        # ]),
        # html.Br(),
        # html.Div([
            html.Iframe(id='x_axis_label', width='1250', height='1000')
        # ])
    ],
    style=CONTENT_STYLE,
    fluid=False
)


# ---------------------call back-------------------


@callback(
        Output('x_axis_label', 'srcDoc'),
        [Input('feature', 'value')]
)
def update_plots(x_label):
    color = ["#fb5607", "#ffd60a", "#15616d", "#540b0e"]
    domain_ = ["Entire home/apt", "Private room", "Shared room", "Hotel room"]
    click = alt.selection_multi(fields=['room_type'], bind='legend')
    brush = alt.selection_interval(resolve='intersect')
    int1 = alt.Chart(airbnb_data).mark_rect(color='orange').encode(
        x=alt.X("room_type", title="Room Type", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        y=alt.Y("city", title="City", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        color=alt.condition(
            brush,
            alt.Color('count()',scale=alt.Scale(scheme='goldorange')),
            alt.value('lightgray')),
      tooltip = ["count()"]
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
            alt.Color('room_type:N',scale=alt.Scale(domain=domain_,range=color)),
            alt.value('rgba(240, 240, 240, 0.1)')
        ),
        tooltip=["mean(Rating)", "city"]
    ).add_selection(
        brush
    )

    bars = (alt.Chart(airbnb_data).mark_bar().encode(
        x=alt.X('count()', title="Count", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        y=alt.Y('city', title="City", axis=alt.Axis(labelAngle=0, titleFontSize=15, labelFontSize=13)),
        color= alt.Color('room_type:N',title="Room  Types",scale=alt.Scale(domain=domain_,range=color)),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)), tooltip=["count()"])
            .transform_filter(brush))

    chart = int1.properties(height=450, width=450) | (int2 & bars).add_selection(
        click
    )
    return chart.to_html()



