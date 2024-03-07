import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from dash_table import DataTable
dash.register_page(__name__, suppress_callback_exceptions=True, path='/')
# ---------------------import data-------------------
listings=pd.read_csv("data/processed/airbnb_data.csv")
# listings=pd.read_csv("/Users/bobbydhada/mds/Data-551/group-proj/airbnb-dashboard/data/processed/airbnb_data.csv")
CITY=listings['city'].unique().tolist()
idx_Van_DT=(listings['city']=='Vancouver')&(listings['neighbourhood']=='Downtown')
default_price_min=listings.loc[idx_Van_DT, 'price'].min()
default_price_max=listings.loc[idx_Van_DT, 'price'].max()
default_listing_count=listings.loc[idx_Van_DT, ].shape[0]

default_hosts_vancouver = listings.loc[idx_Van_DT, ['host_name', 'host url', 'rating']]
default_hosts_grouped = default_hosts_vancouver.groupby('host_name')['rating'].mean().reset_index()
# Assuming host_url is a column in your DataFrame
hosts_average = default_hosts_vancouver[['host_name', 'rating', 'host url']].copy()
# Merge the grouped mean ratings with the original DataFrame
hosts_average = hosts_average.merge(default_hosts_grouped, on='host_name', suffixes=('', '_mean'))
# Rename columns for clarity
hosts_average = hosts_average.rename(columns={'rating_mean': 'average_rating'})
hosts_average.sort_values(by=['average_rating'], ascending=False, inplace=True)
hosts_average.dropna(inplace=True)
hosts_average = hosts_average.iloc[0:5]
default_hosts = hosts_average[['host_name', 'host url']]
# ---------------------content style-------------------
CONTENT_STYLE = {
    "margin-left": "0%",
    "margin-right": "0%",
    # "padding": "2rem 1rem",
    # 'height' : '100%',
    # "width": "90%", 
    # "margin": "0 auto",
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
    className='card',
    style={
                    'width': '160%',
                    'margin-left': '0%' 
                #     'height': '950px', 
                #     'margin':'auto',
                 }
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
    className='card',
    style={
                    'width': '130%',
                    'margin-left': '45%' 
                #     'height': '950px', 
                #     'margin':'auto',
                 }
)
price_slider=dbc.Card([
    dbc.CardHeader("Price Range (CAD)",
                   style={'font-size':'18px',
                          'background':'rgba(0,0,0,0)',
                          'textAlign':'center'}),
    dbc.CardBody([
        dcc.RangeSlider(id='price',
                        min=default_price_min,
                        max=default_price_max,
                        value=[default_price_min, default_price_max],
                        #marks={default_price_min: f'${default_price_min}', default_price_max: f'${default_price_max}'},
                        #marks=None,
                        
                        tooltip={
                            #'updatemode': 'mouseup',# or 'drag', invalid for unkown reason
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

number=dbc.Card(
    dbc.CardBody([
        html.H1("Number of Listings", className='card-title', style={'textAlign': 'center'}),
        html.Hr(),
        html.H1(str(default_listing_count),
                id='listing_count',
                style={
                    'textAlign' : 'center',
                    'color' : '#FF9874',
                    'fontSize': 50
                })
    ]),
    className='card',
    style={
                    'width': '103.5%',
                    'margin-left': '0%',
                    'height': '100%' 
                #     'height': '950px', 
                #     'margin':'auto',
                 }
)
listing_map=dbc.Card([dcc.Graph(id='listing_map', 
                                  style={'width': '100%', 
                                         'height': '100%'}
                            )
                ],
                className= 'card map-card',
                style={
                    'width': '98%',
                    'margin-left': '2.8%', 
                    'height': '200%',
                    #'margin-right': '100%' 
                #     'margin':'auto',
                 }
                )

hosts = dbc.Card([
    dbc.CardBody([DataTable(
        id='hosts-table',
        columns=[
            {'name': 'Top Hosts', 'id': 'host_name', 'presentation': 'markdown'},
        ],
        data=default_hosts.to_dict('records'),
        style_table={'height': '100%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center', 'fontSize':'20px'},
        style_as_list_view = True
        )
    ])], style={
                    'width': '103.5%',
                    'margin-left': '0%',
                    'height':'100%' 
                #     'height': '950px', 
                #     'margin':'auto',
                 })
# ---------------------layout-------------------
layout=dbc.Container(
    children=[
        dbc.Stack([
            dbc.Stack([
                dbc.Stack([
                    html.Br(),
                    html.H1("Listing Map", style={"textAlign": "center", 'color' : '#FF9874', 'fontSize': 55, "textShadow": "2px 2px 2px #000000"}),
                    html.Br()]),
                dbc.Stack([
                    html.Div(city),  # Set width to 6 for half the row
                    html.Div(neighbourhood)  # Set width to 6 for half the row
                ], direction = 'horizontal'),
                dbc.Stack([
                    html.Div(price_slider),
                    html.Div(number),
                    html.Div(hosts)], gap =1)
            ], gap = 1),  # Set width to 6 for half the container
            dbc.Stack(listing_map)  # Set width to 6 for half the container
        ], direction = 'horizontal')
    ],
    style=CONTENT_STYLE,
    fluid=False,
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
    Output('hosts-table', 'data'),
    [ Input('city', 'value'),
     Input('neighbourhood', 'value'),
     Input('price', 'value')]
)
def update_table(neighbourhood, city, price_range):
    if neighbourhood != None:
        idx = (listings['neighbourhood'] == city) & (listings['city'] == neighbourhood) & (listings['price'].between(price_range[0], price_range[1]))
    else:
        idx = (listings['neighbourhood'] == city) & (listings['price'].between(price_range[0], price_range[1]))
    data_filtered = listings.loc[idx, ['host_name', 'host url', 'rating']]
    default_hosts_grouped = data_filtered.groupby('host_name')['rating'].mean().reset_index()
    # Assuming host_url is a column in your DataFrame
    hosts_average = data_filtered[['host_name', 'rating', 'host url']].copy()
    # Merge the grouped mean ratings with the original DataFrame
    hosts_average = hosts_average.merge(default_hosts_grouped, on='host_name', suffixes=('', '_mean'))
    # Rename columns for clarity
    hosts_average = hosts_average.rename(columns={'rating_mean': 'average_rating'})
    hosts_average.sort_values(by=['average_rating'], ascending=False, inplace=True)
    hosts_average.dropna(inplace=True)
    hosts_average = hosts_average.iloc[0:5]
    final_data = hosts_average[['host_name', 'host url']]
    hosts_data = final_data.to_dict('records')
    # Format the host names as clickable links
    n = 1
    for row in hosts_data:
        row['host_name'] = f"{n}. [{row['host_name']}]({row['host url']})"
        n += 1
    return hosts_data

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
        idx=(listings['city']==city)&(listings['price'].between(price_range[0], price_range[1]))
        zoom_size=12
    map_data=listings.loc[idx, ]
    center_lat=map_data['latitude'].mean()
    center_lon=map_data['longitude'].mean()
    map_data['By'] = map_data.apply(lambda row: f'<a href="{row["host url"]}">{row["host_name"]}</a>', axis=1)
    map_data['Listing'] = map_data.apply(lambda row: f'<a href="{row["url"]}">{"Visit Link"}</a>', axis=1)
    map_data['price'] = map_data['price'].apply(lambda x: f"${x} CAD")
    map_data['Details'] = map_data.apply(lambda row: f"{row['name']}<br>Listing: {row['Listing']}<br>By: {row['By']} <br>Price: {row['price']}", axis=1)
    fig=px.scatter_mapbox(
        data_frame=map_data,
        lat='latitude',
        lon='longitude', #{'name', 'By', 'rating', 'Listing', 'price'},
        zoom=zoom_size,
        center=dict(lat=center_lat, lon=center_lon)
    )
    
    fig.update_traces(marker=dict(color='#FF5B4B', size = 8), hovertemplate = map_data['Details'])
    
    fig.update_layout(
        mapbox_style='open-street-map',
        margin={"r":0,"t":0,"l":0,"b":0},  # Set margins
        hovermode='closest',
        hoverlabel=dict(namelength=350, bgcolor='white', font_family = 'Rockwell', font_size = 16))
    return fig
