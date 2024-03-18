import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
dash.register_page(__name__, path='/statistics')

# Import dataset

airbnb_data = pd.read_csv("data/processed/airbnb_data.csv")
alt.data_transformers.enable('default', max_rows=None)
airbnb_data['rating'] = pd.to_numeric(airbnb_data['rating'])
roomtypes = airbnb_data['room_type'].unique().tolist()
# Content Style

CONTENT_STYLE = {
    "margin-left": "0%",
    "margin-right": "0%",
    "padding": "2rem 1rem",
}

MD_STYLE = {
    'size': '1232',
}

# App Components

slider_price = dbc.Card([
    dbc.CardHeader("Price Range (CAD)",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)',
                          'textAlign':'center'}),
    dbc.CardBody([
        dcc.RangeSlider(id='slider_price',
                        min=0,
                        max=1000,
                        value=[0, 1000],
                        
                        tooltip={
                            'placement': 'bottom',
                            'always_visible' : True,
                        }, 
                        )
    ])
],
    className='card',
    style={
                    'width': '103.5%',
                    'margin-left': '0%', 
                     'height': '100%' 
                #     'margin':'auto',
                 }
)

# Layout
layout = dbc.Container(
    children=[
        html.H1('Room Type Insights', style={"textAlign": "center", 'color' : '#FF9874', 'fontSize': 55, "textShadow": "2px 2px 2px #000000"}),
        html.P('Explore room types with dynamic price filtering for insightful booking decisions.', style={"textAlign": "center"}),
        html.Hr(),
        dbc.Stack([
            dbc.Stack([
                html.Iframe(id='bar-plot', width='600', height='300'),
                html.Iframe(id='vp', width='600', height='380')    
            ]),
            dbc.Stack([
                dbc.Card([
                    dbc.CardHeader("Listings Distribution",
                    style={'font-size':'35px',
                          'background':'#FF9874',
                          'textAlign':'center',
                          "font-family": "Roboto"}),
                    dcc.Markdown(id='percentages', className='md-percentages', style={'font-size': '30px', "font-family": "Roboto"})
                ]),
                html.Div([
                    slider_price
                ], style = {'width': '96%'})
            ], gap=3)
        ], direction='horizontal')
    ],
    style=CONTENT_STYLE,
    fluid=True
)


# Callbacks

@callback(
    Output('vp', 'srcDoc'),
    [Input('slider_price', 'value')]
)
def update_violin_plot(choice):
    if choice == None:
        min_value = airbnb_data.price.min()
        max_value = airbnb_data.price.max()
    else:
        min_value, max_value = choice
    rating_df = airbnb_data[(airbnb_data.price >= min_value) & (airbnb_data.price <= max_value)]

    vp = alt.Chart(rating_df).transform_density("price", as_=["price", "density"], extent=[0, 1000],
                                                groupby=["room_type"]).mark_area(
        orient='horizontal').encode(
        x = alt.X('density:Q', stack='center', impute=None, title=None, axis = alt.Axis(labels=False, values=[0], grid=False, ticks=True)),
        y = alt.Y('price:Q', title='Price', axis=alt.Axis(titleFontSize=15, labelFontSize=13, format='$.3s')),
        color = alt.Color('room_type:N'),
        column = alt.Column('room_type:N', spacing=0, header= alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=0,titleFontSize=15,labelFontSize=13,title='Room Type')),
        tooltip="price"
    ).properties(
        height=280,
        width=120
    ).configure_legend(
       disable=True
    ).configure_view(
        stroke=None
    )
    return vp.to_html()

@callback(
    Output('bar-plot', 'srcDoc'),
    [Input('slider_price', 'value')]
)
def update_bar_plot(values):
    if values == None:
        min_value = airbnb_data.price.min()
        max_value = 1000
    else:
        min_value, max_value = values
    data = airbnb_data[(airbnb_data.price >= min_value) & (airbnb_data.price <= max_value)]
    
    bar_plot = alt.Chart(data).mark_bar().encode(
        x = alt.X('room_type', title=None),
        y = alt.Y('count()', title='Number of Listings'),
        color = alt.Color('room_type'),
        tooltip = alt.Tooltip('count()')
    ).properties(
        height=225,
        width = 500
    ).configure_axisX(
        labelAngle=0
    ).configure_legend(
       disable=True
    )
    
    return bar_plot.to_html()

@callback(
    Output('percentages', 'children'),
    [Input('slider_price', 'value')]
)
def update_pie_chart(values):
    if values == None:
        min_value = airbnb_data.price.min()
        max_value = 1000
    else:
        min_value, max_value = values
    data = airbnb_data[(airbnb_data.price >= min_value) & (airbnb_data.price <= max_value)]
    
    listings_percentage = {}
    total_listings = data['room_type'].count()
    for roomtype in roomtypes:
        percentage = round(data[data['room_type'] == roomtype]['room_type'].count() / total_listings * 100, 2)
        listings_percentage[roomtype] = percentage
    response = f'''
        - **{roomtypes[0]}**: {listings_percentage[roomtypes[0]]}%
        - **{roomtypes[1]}**: {listings_percentage[roomtypes[1]]}%
        - **{roomtypes[2]}**: {listings_percentage[roomtypes[2]]}%
        - **{roomtypes[3]}**: {listings_percentage[roomtypes[3]]}%
    '''
    return response