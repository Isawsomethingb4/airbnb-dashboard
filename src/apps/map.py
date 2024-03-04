import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
dash.register_page(__name__, suppress_callback_exceptions=True, path='/')
# ---------------------import data-------------------
listings=pd.read_csv("../data/processed/airbnb_data.csv")
# listings=pd.read_csv("/Users/bobbydhada/mds/Data-551/group-proj/airbnb-dashboard/data/processed/airbnb_data.csv")
CITY=listings['city'].unique().tolist()
idx_Van_DT=(listings['city']=='Vancouver')&(listings['neighbourhood']=='Downtown')
default_price_min=listings.loc[idx_Van_DT, 'price'].min()
default_price_max=listings.loc[idx_Van_DT, 'price'].max()
default_listing_count=listings.loc[idx_Van_DT, ].shape[0]
# ---------------------content style-------------------
CONTENT_STYLE = {
    # "margin-left": "30rem",
    # "margin-right": "2rem",
    # "padding": "2rem 1rem",
    'height' : '100%',
    "width": "90%", 
    "margin": "0 auto",
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
    body=True,
    className='card'
)
neighbourhood=dbc.Card(
    [
        html.Div([
            dbc.Label('Neighbourhood'),
            dcc.Dropdown(
                id='neighbourhood',
                #value='Downtown' not everycity has a downtoen, callback needed here
            )
        ])
    ],
    body=True,
    #style={'width' : '350px'}
    className='card'
)
price_slider=dbc.Card([
    dbc.CardHeader("Price Range($)",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)'}),
    dbc.CardBody([
        dcc.RangeSlider(id='price',
                        min=default_price_min+15,
                        max=default_price_max+15,
                        value=[default_price_min+15, default_price_max+15],
                        #marks={default_price_min: f'${default_price_min}', default_price_max: f'${default_price_max}'},
                        marks=None,
                        tooltip={
                            #'updatemode': 'mouseup',# or 'drag', invalid for unkown reason
                            'placement': 'bottom',
                            'always_visible' : True,
                        }
                        )
    ])
],
    className='card ',
    style={
            'width': '950px'}
)

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
    className='card'
)
listing_map=dbc.Card([
                    dbc.CardHeader("Listings Across Canada 🍁"),
                    dcc.Graph(id='listing_map', 
                                  style={'width': '100%', 
                                         'height': '100%'}
                            )
                ],
                className= 'card map-card',
                style={
                    'width': '1650px', 
                #     'height': '950px', 
                #     'margin':'auto',
                 }
                )
# ---------------------layout-------------------
layout=dbc.Container(
    children=[
        html.H1("Listing Map", style={"textAlign": "center"}),
        html.P("Explore Airbnb listings geographically and gain valuable insights at a glance.", style={"textAlign": "center"}),
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
            html.Br(), 
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
# decide neighbourhood default value with city
@callback(
        Output('neighbourhood', 'value'),
        [Input('city', 'value')]
)
def update_default_neighbourhood(city):
    neighbourhoods=sorted(listings.loc[listings['city']==city, 'neighbourhood'].unique().tolist())
    if 'Downtown' in neighbourhoods:
        return 'Downtown'
    else:
        return neighbourhoods[0]

# decide neighbourhood with city
@callback(
    Output('neighbourhood', 'options'),
    [Input('city', 'value')]
)
def update_neighbourhood(city):
    neighbourhoods=sorted(listings.loc[listings['city']==city, 'neighbourhood'].unique().tolist())
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
    range=[min_price, max_price + 15]
    return min_price, max_price + 15, range
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
        idx=(listings['city']==city)&(listings['price'].between(price_range[0], price_range[1]))
    count=listings.loc[idx, ].shape[0]
    return count
# the map plot
@callback(
    Output('listing_map', 'figure'),
    [Input('city', 'value'),
     Input('neighbourhood', 'value'),
     Input('price', 'value')]
)
def update_map(city, neighbourhood, price_range):
    # Filter the listings based on selected values
    unique_neighbourhoods = listings.loc[listings['city'] == city, 'neighbourhood'].unique()
    if neighbourhood is not None and neighbourhood in unique_neighbourhoods:
        idx = (listings['city'] == city) & (listings['neighbourhood'] == neighbourhood) & (listings['price'].between(price_range[0], price_range[1]))
        zoom_size = 14
    else:
        idx = (listings['city'] == city) & (listings['price'].between(price_range[0], price_range[1]))
        zoom_size = 12
    map_data = listings.loc[idx, ['latitude', 'longitude', 'name', 'price', 'host_name', 'host url', 'url']]
    map_data.dropna(inplace=True)
    center_lat = map_data['latitude'].mean()
    center_lon = map_data['longitude'].mean()
    # Create a new scatter_mapbox figure
    fig = go.Figure(go.Scattermapbox(
        lat=map_data['latitude'],
        lon=map_data['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            cmin = price_range[0],
            cmax = price_range[1],
            color = map_data['price'],
            colorscale = [[0, 'blue'], [1, 'red']],
            colorbar = dict(title='Price')
        ),
        text=[f'{name}<br>Price: ${price}<br>By: <a href="{host_url}" target="_blank">{host_name}</a><br><a href="{url}" target="_blank">Visit Link</a>' for name, url, host_name, host_url, price in zip(map_data['name'], map_data['url'], map_data['host_name'], map_data['host url'], map_data['price'])],
        hoverinfo='text'
    ))
    # Update layout properties
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_size
        )
    )
    return fig