import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.express as px
dash.register_page(__name__, suppress_callback_exceptions=True, path='/')


# ---------------------import data-------------------
listings=pd.read_csv("../data/processed/airbnb_data.csv")
CITY=listings['city'].unique().tolist()
idx_Van_DT=(listings['city']=='Vancouver')&(listings['neighbourhood']=='Downtown')
default_price_min=listings.loc[idx_Van_DT, 'price'].min()
default_price_max=listings.loc[idx_Van_DT, 'price'].max()
default_listing_count=listings.loc[idx_Van_DT, ].shape[0]

# ---------------------content style-------------------
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# ---------------------app components-------------------
city=dbc.Card(
    [
        html.Div([
                dbc.Label("City"),# label to display
                dcc.Dropdown(
                    id='city',
                    options=[
                        {'label': city, 'value': city} for city in CITY
                    ],
                    value='Vancouver'
                )
            ])
    ],
    body=True
)
neighbourhood=dbc.Card(
    [
        html.Div([
            dbc.Label('Neighbourhood'),
            dcc.Dropdown(
                id='neighbourhood',
                value='Downtown'
            )
        ])
    ],
    body=True,
    style={'width' : '350px'}
)
price_slider=dbc.Card([
    dbc.CardHeader("Price Range($)",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody([
        dcc.RangeSlider(id='price',
                        min=default_price_min,
                        max=default_price_max,
                        value=[default_price_min, default_price_max],
                        #marks={default_price_min: f'${default_price_min}', default_price_max: f'${default_price_max}'},
                        marks=None,
                        tooltip={
                            #'updatemode': 'mouseup',# or 'drag', invalid for unkown reason
                            'placement': 'bottom',
                            'always_visible' : True,
                        }
                        
                        )
    ])
])
number=dbc.Card(
    dbc.CardBody([
        html.H1("Number of Listings", className='card-title'),
        html.Hr(),
        html.Br(),
        html.H1(str(default_listing_count),
                id='listing_count',
                style={
                    'textAlign' : 'center',
                    'color' : 'grey'
                })
    ]),
    color='primary',
    style={"height": "270px", "width": "500px"},
)
listing_map=dbc.Card([
                    dbc.CardHeader("Listings Across Canada 🍁"),
                    dbc.CardBody([
                        # html.Iframe(id='listing_map', 
                        #             srcDoc=map_example.to_html(), 
                        #             style={'border_width' : '0', 'width' : '100%', 'height' : '100%'})
                        dcc.Graph(id='listing_map', 
                                  className="h-100",
                                  style={'width': '100%', 'height': '100%'})
                    ], style={'width': '100%', 'height': '100%'})
                ],
                style={
                    'border-radius' : '2%',
                    'width': '1650px', 
                    'height': '950px', 
                    # 'margin':'auto'
                    #'width': '100%', 'height': '100%' size problem here
                }
                )

# ---------------------layout-------------------
layout=dbc.Container(
    children=[
        html.H1("Welcome to Airbnb Dashboard"),
        html.P("This is some introductory text about this map tab"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                        dbc.Col(city),
                        dbc.Col(neighbourhood)
                    ]),
                html.Br(),
                dbc.Row(price_slider)
                ]),
            dbc.Col(number)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(listing_map)
        ])
    ],
    style=CONTENT_STYLE,
    fluid=False
)


# ---------------------call back-------------------   
# decide neighbourhood with city
@callback(
    Output('neighbourhood', 'options'),
    [Input('city', 'value')]
)
def update_neighbourhood(city):
    neighbourhoods=listings.loc[listings['city']==city, 'neighbourhood'].unique().tolist()
    options=[{'label': neighbourhood, 'value': neighbourhood} for neighbourhood in neighbourhoods]
    return options

# decide price range according to city and neighbourhood
@callback(
    [Output('price', 'min'),
    Output('price', 'max'),
    Output('price', 'value')],
    [Input('city', 'value'),
    Input('neighbourhood', 'value')]
)
def update_price_range(city, neighbourhood):
    if neighbourhood!=None:
        idx=(listings['city']==city)&(listings['neighbourhood']==neighbourhood)
    else:
        idx=listings['city']==city
    price=listings.loc[idx, 'price']
    min_price=price.min()
    max_price=price.max()
    range=[min_price, max_price]
    return min_price, max_price, range 

# display listing count according to city and neighbourhood
@callback(
    Output('listing_count', 'children'),
    [Input('city', 'value'),
     Input('neighbourhood', 'value'),
     Input('price', 'value')]
)
def update_listing_count(city, neighbourhood, price_range):
    if neighbourhood!=None:
        idx=(listings['city']==city)&(listings['neighbourhood']==neighbourhood)&(listings['price'].between(price_range[0], price_range[1]))
    else:
        idx=idx=(listings['city']==city)&(listings['price'].between(price_range[0], price_range[1]))
    count=listings.loc[idx, ].shape[0]
    return count


# the map plot
@callback(
    Output('listing_map', 'figure'),
    [Input('city', 'value'),
     Input('neighbourhood', 'value'),
     Input('price', 'value')]
)
def plot_map(city, neighbourhood, price_range):
    if neighbourhood!=None:
        idx=(listings['city']==city)&(listings['neighbourhood']==neighbourhood)&(listings['price'].between(price_range[0], price_range[1]))
        zoom_size=14
    else:
        idx=(listings['city']==city)&(listings['price'].between(price_range[0], price_range[1]))
        zoom_size=12
    map_data=listings.loc[idx, ['latitude', 'longitude']]
    center_lat=map_data['latitude'].mean()
    center_lon=map_data['longitude'].mean()
    fig=px.scatter_mapbox(
        data_frame=None,
        lat=map_data['latitude'],
        lon=map_data['longitude'],
        zoom=zoom_size,
        center=dict(lat=center_lat, lon=center_lon)
    )
    fig.update_layout(
        mapbox_style='open-street-map',
        margin={"r":0,"t":0,"l":0,"b":0}  # Set margins
    )
    return fig