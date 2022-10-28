###----------------------LIBRARIES----------------------------###
from ast import In
from msilib.schema import Component
from tarfile import USTAR_FORMAT
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash_bootstrap_components as dbc # pip install dash_bootstrap_components
from dash import Dash, dcc, html, Input, Output, State   # pip install dash (version 2.0.0 or higher)


###-----------------LOADING & PREPARING DATA----------------------------###
#Setting a DataFrame
df = pd.read_csv('data.csv')
df.drop_duplicates(keep = 'first', inplace = True)
df.usage_date = df.usage_date.apply(lambda x: dt.datetime.strptime(x.split()[0], '%Y-%m-%d'))
df.user_created_date = df.user_created_date.apply(lambda x: dt.datetime.strptime(x.split()[0], '%Y-%m-%d')if x is not np.nan else x)
df = df.set_index('usage_date',drop = True)[['cust_id', 'source_duration', 'transcoded_duration', 'video_duration',"user_created_date"]].sort_index(ascending = True)
df['new_customer'] = df.user_created_date.apply(lambda x: True if x > df.index[-1] - dt.timedelta(days = 90)
                                                                  else False)



###-------------------------------------- CONSTANTS -------------------------------------------------------###
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)
#app = Dash(__name__)

# Standard Colors
color_font = 'rgb(243,247,246)'
color_background = 'rgb(31,38,48)'
color_container = 'rgb(37,46,63)'
clear_color_chart = 'rgb(38,254,184)'
dark_color_chart = 'rgb(41,152,119)'

# Chart Tamplate
layout = go.Layout(
        autosize=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        grid = None,
        plot_bgcolor=color_background,
        paper_bgcolor=color_container,
        legend=dict(font=dict(size=10), orientation="h"),
        title="Title Name",
        font = dict(
                size = 12,
                color = color_font))

#Filter paramters
#Date Granularity - Dropdown List
date_granularity = {'Day': 'D', 'Month': 'M', 'Year': 'Y'}

#end and start date
start_date = dt.date(2022,1,1)
end_date = dt.date(2022,10,21)

# Top N - Dropdown List
top =  [5,10,15,20]
###--------------------------------- DASH COMPONENTS - LAYOUT----------------------------------------###

app.layout = html.Div([
     dcc.Store(id="aggregate_data", data = [], storage_type = 'memory'),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        #Header
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.svg"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                #Title
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Livepeer Customer Usage",
                                    style={"margin-bottom": "0px",
                                        "margin-right": "300px",
                                        "align-items":"flex-start",
                                        "color": "rgb(38,254,184)"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title")
        ],style = {'margin-top': '0%'}),
        #Filters division
        html.Div(
            [
                html.Div([
                    #Date Picker
                    html.P('Date Range', className = 'control_label'),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed= start_date,
                        max_date_allowed = end_date,
                        start_date = start_date,
                        end_date= end_date,
                        display_format = "MM/DD/YYYY",
                        start_date_placeholder_text = "MM/DD/YYYY",
                        style = {'width':'50%'},
                        className = 'dcc_control'),

                    #Date Granunality
                    html.P("Date Granularity", className = 'control_label'),
                    dcc.Dropdown(
                        id = 'granunality-drop',
                        options= [{"label": i, "value": i} for i in ['Day','Month','Year']],
                        value = 'Day',
                        clearable = False,
                        style = {'width':'60%'},
                        className = 'dcc_control'),
                        
                    #Ranking
                    html.P("Ranking Top Users", className = 'control_label'),
                    dcc.Dropdown(
                        options = [{"label": i, "value": i} for i in top],
                        id = 'rank-drop',
                        clearable = False,
                        value = 5,
                        style = {'width':'30%'},
                        className = 'dcc_control')],
                    #Customize
                    #html.P("Customers", className = 'control_label'),
                    #dcc.Dropdown(
                     #   id="customers-drop",
                      #  options= [{"label": i, "value": i} for i in list(set(df.cust_id.to_list())) +['All']],
                       # value = 'All',
                        #clearable = False,
                        #multi= False,   
                        #style = {'width':'50%'},
                        #className="dcc_control",
                        #)
                #],
                className="pretty_container twelve columns",
                id="cross-filter-options"
                )        
        ] ),
        #Big Numbers Section
            html.Div([
                 html.Div([
                    html.Div
                    ([],
                        id="transcode",
                        className="mini_container",
                    ),
                    html.Div(
                        [],
                        id="source",
                        className="mini_container",
                    ),
                    html.Div(
                        [],
                        id="video",
                        className="mini_container",
                    )
                ],
                style = {'display': 'flex', 'width': '100%'},
                id="info-container"
               
                ),
            ], style = {'display':'inline-block'}),
        
        #Tab Section
        html.Div([
                html.Div([
                    dcc.Tabs([
                        dcc.Tab(label = 'Transcoded Duration', value = 'transcoded_duration'),
                        dcc.Tab(label = 'Source Duration', value = 'source_duration'),
                        dcc.Tab(label = 'Video Duration', value = 'video_duration')
                    ],
                    id ='tabs',
                    value = 'transcoded_duration',
                    style = {'width': 'auto', 'margin': '12px'},
                    className = "pretty_container twelve columns"),
                html.Div([
                    
                ],
                id = 'tabs-content-graphs')

                ])
        ])
])

####-------------------------------- CONNECTING PLOTLY GRAPHS WITH DASH COMPONENTS--------------####
# Date granunality, Date range, clients
@app.callback(  
    Output(component_id = "aggregate_data", component_property = 'data'),
    [Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
    Input(component_id = 'my-date-picker-range', component_property = 'end_date'),
    Input(component_id = 'granunality-drop', component_property = 'value')]
)

def data_filtered(start_date,end_date,time):
    
    df_filter = df.loc[start_date:end_date].to_period(date_granularity[time]).reset_index()
    df_filter = df_filter.reset_index(drop = True)
    df_filter.usage_date = df_filter.usage_date.apply(lambda x: x.to_timestamp())
    data_dict = df_filter.to_dict(orient = 'record')

    return data_dict

#Big Numbers
@app.callback(
    [Output('transcode', 'children'),
    Output('source', 'children'),
    Output('video', 'children')],
    [Input("aggregate_data",'data')],prevent_initial_call=True)

def display_numbers(json_dict):
    #Converting Json dict to dataframe
    df = pd.DataFrame(json_dict)
    df = df.set_index('usage_date')
    # Metrics Accumulated
    df_total = df.sum(axis = 0, numeric_only = True)

    def format_num(text,numb):
        return html.Div([
                html.P(text, className = "text-big-numbers"),
                html.Br(),
                html.P(numb, className = "big-numbers"),
                ])
    transcode = format_num("Transcoded Duration",df_total['transcoded_duration'])
    source = format_num("Source Duration",df_total['source_duration'])
    video = format_num("Video Duration",df_total['video_duration'])

    return transcode, source, video


#Tabs, Top customers
@app.callback(
    Output(component_id = 'tabs-content-graphs', component_property = 'children'),
    [Input(component_id = 'tabs', component_property = 'value')],
    [Input(component_id = 'rank-drop', component_property = 'value')],
    [Input(component_id = "aggregate_data", component_property = 'data')],prevent_initial_call=True)

def render_content(tab,N,json_dict):

    #Converting Json dict to dataframe
    df = pd.DataFrame(json_dict)
    df = df.set_index('usage_date')

#Defining  Graph Objects
    # Metrics Over Time
    df_overtime = df.groupby(by = 'usage_date').agg({'source_duration': np.sum,
                                                        'transcoded_duration': np.sum,
                                                        'video_duration': np.sum})
    fig_overtime = go.Figure(data = [go.Bar(x = df_overtime.index, y = df_overtime[tab])], layout = layout)
    fig_overtime.update_traces(marker_color = clear_color_chart)
    fig_overtime.update_layout(title_text='{} - Over Time '.format(" ".join(tab.split('_')).capitalize()))

    # Metrics Total Running
    df_cumsum = df.groupby(by = 'usage_date').agg({'source_duration': np.sum,
                                                      'transcoded_duration': np.sum,
                                                      'video_duration': np.sum}).cumsum(axis =0)                                                     
    fig_total_running= go.Figure(layout = layout)
    fig_total_running.add_trace(go.Scatter(x =df_cumsum.index,y = df_cumsum[tab], fill='tozeroy'))
    fig_total_running.update_traces(marker_color= clear_color_chart, marker_line_color= dark_color_chart,
                  marker_line_width=1.5, opacity=0.6)
    fig_total_running.update_layout(title_text='{} - Total Running '.format(" ".join(tab.split('_')).capitalize()))

    # Metrics Variation Overtime
    df_pct_change = df.groupby(by = 'usage_date').agg({'source_duration': np.sum,
                                    'transcoded_duration': np.sum,
                                    'video_duration': np.sum}).pct_change().drop(df.index[0],axis = 0).replace(np.inf,1)
    fig_pct_change = go.Figure(layout= layout)
    fig_pct_change.add_trace(go.Scatter(x = df_pct_change.index, y = df_pct_change[tab], mode = 'lines', name = 'lines'))
    fig_pct_change.update_traces(marker_color = clear_color_chart)

    # Histogram
    fig_hist = go.Figure(data = [go.Histogram(x = df[tab], nbinsx = 200)], layout = layout)
    fig_hist.update_traces(marker_color = dark_color_chart)
    fig_hist.update_layout(title_text='{} - Histogram of Customer Usage'.format(" ".join(tab.split('_')).capitalize()))

    #Ranking Chart
    df_rank = df.groupby(by = 'cust_id').agg({'source_duration': np.sum,
                                        'transcoded_duration': np.sum,
                                        'video_duration': np.sum})[[tab]].sort_values(by =tab, ascending = False)
    df_top = df_rank.copy()                                    
    df_top['ranking'] = range(1,len(df_top.index) +1)
    df_top = df_top.iloc[:N,:].reset_index().assign(rank_id = lambda x: x['ranking'].apply(lambda x: str(x) + ' - ') + x['cust_id'])
    colors = [dark_color_chart] * N
    colors[0] = 'crimson'
    fig_rank = go.Figure(data = [go.Bar(x = df_top['rank_id'], y = df_top[tab], marker_color = colors)], layout = layout)
    fig_rank.update_layout(title_text='Top {} Customers by {}'.format(N," ".join(tab.split('_')).capitalize()))

    #Ranking charts for future potencials
    #Dataframe for new clients - Clients who created  their account within the last 3 months
    df_potencial = df.copy()
    df_new = df_potencial[df_potencial.new_customer == True]

    df_rank_new = df_new.groupby(by = 'cust_id').agg({'source_duration': np.sum,
                                        'transcoded_duration': np.sum,
                                        'video_duration': np.sum})[[tab]].sort_values(by =tab, ascending = False)                                
    df_rank_new ['ranking'] = range(1,len(df_rank_new.index) +1)
    df_rank_new  = df_rank_new .iloc[:N,:].reset_index().assign(rank_id = lambda x: x['ranking'].apply(lambda x: str(x) + ' - ') + x['cust_id'])
    colors = [dark_color_chart] * N
    colors[0] = 'crimson'
    fig_rank_new = go.Figure(data = [go.Bar(x = df_rank_new['rank_id'], y = df_rank_new[tab], marker_color = colors)], layout = layout)
    fig_rank_new.update_layout(title_text='Top {} New Customers by {} (New customers in the past 3 months)'.format(N," ".join(tab.split('_')).capitalize()), title_font_size = 14)
    #Return Graphs 
    return html.Div([
                html.Div([
                    html.Div(
                        [dcc.Graph(figure = fig_overtime,id="overtime-graph",
                                                                style = {'width':'auto',
                                                                        'height': '100%',
                                                                        'margin': '10px'})],
                    ),
                    html.Div(
                        [dcc.Graph(figure = fig_rank, id="total-running-grapth",style ={'width':'auto',
                                                                    'height': '100%',
                                                                    'margin': '10px'})],
                    ),
                    html.Div(
                        [dcc.Graph(figure = fig_hist,id="total-running-grapth",style ={'width':'auto',
                                                                    'height': '100%',
                                                                    'margin': '10px'})]
                    ),
                ], className = 'six columns'),
                html.Div([
                    html.Div(
                        [dcc.Graph(figure = fig_total_running, id="overtime-graph",style = {'width':'auto',
                                                                'height': '100%',
                                                                'margin': '10px'})],
                    ),
                    html.Div(
                        [dcc.Graph( figure = fig_rank_new, id="total-running-grapth",style ={'width':'auto',
                                                                    'height': '100%',
                                                                    'margin': '10px'})],
                    ),
                    html.Div(
                        [dcc.Graph(figure = fig_pct_change, id="total-running-grapth",style ={'width':'auto',
                                                                    'height': '100%',
                                                                    'margin': '10px'})]
                    )
                ], className = 'six columns')    
            ], className="pretty_container twelve columns")

if __name__ == '__main__':
    app.run_server(debug=True)