import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
import psycopg2
import psycopg2.extras
import pandas.io.sql as psql
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

conn = psycopg2.connect(
    database="newsLeader",
    user="postgres",
    password="Tianya1990",
    host="liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com",
    port='5432'
)

df = "global"

df = psql.read_sql("""SELECT * FROM public.news2020 ORDER BY "ArticleCounts" DESC LIMIT 10;""", conn)
# df = psql.read_sql("""SELECT * FROM public.newsbase WHERE "EventDateTime" BETWEEN 20191219 AND 20200125 ORDER BY "ArticleCounts" DESC LIMIT 10;""", conn)
df['EventDateTime'] = pd.to_datetime(df['EventDateTime'], format='%Y%m%d', errors='coerce')
df.EventDateTime = pd.DatetimeIndex(df.EventDateTime).strftime("%Y-%m-%d")
df = df.drop(columns=['IsRootEvent'])
#df.index = df['EventDateTime']

conn = None

def generate_map(dataframe, max_rows=10):
    px.set_mapbox_access_token("pk.eyJ1IjoibHh1MDEiLCJhIjoiY2s2dHp5Z3F4MDRzYTNocG5hbzNvdXZzMiJ9.xceyt17S85YHqeAe9jxVzA")
    return px.scatter_mapbox(df, lat="Latitude", lon="Longitude", \
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, \
        zoom=1)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_plot(dataframe, max_rows=10):
    return dcc.Graph(
            figure={
                "data": [
                    go.Bar(
                        x=list(range(1,11)),
                        y=dataframe['ArticleCounts'],
                        marker={
                            "color": "#97151c",
                            "line": {
                                "color": "rgb(255, 255, 255)",
                                "width": 2,
                            },
                        },
                        name="News leaders",
                    ),
                ], 
            },
        )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
            html.Img(
            src=app.get_asset_url('frontend.png'),
            style={'width': '100%'}
        ),
    ]),

    html.Div([
        html.Div([
            html.H1(children='News Leaders: trace the most reported news events')
        ]),

        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df['EventDateTime'].min(),
                max_date_allowed=df['EventDateTime'].max(),
                initial_visible_month=df['EventDateTime'].min(),
                start_date=df['EventDateTime'].min(),
                end_date=df['EventDateTime'].max(),
                style={'margin-right': '1.5em'}
            ), 
            html.Button('Submit', id='button')
        ]),

        html.Div([
            html.H4(children='Table view'),
            
            html.Div(id='table'),
            
            html.H4(children='Map view'),
            
            dcc.Graph(id='map'),

            html.H4(children='Plot view'),

            html.Div(id="bar-plot"),

            #html.H4(children='Map view'),

            #dcc.Graph(id='map'),

            #html.H4(children='Table view'),
            
            #html.Div(id='table'),

            html.H3(children='Liangchun Xu\tTufts PhD | Insight Data Science')
        ]),
    ], style={'width': '80%','margin': '0 auto', 'text-align': 'center'})   
], style={'margin': '0'}
)

@app.callback([Output('table', 'children'), Output('bar-plot', 'children'),  Output('map', 'figure')],
			 [Input('button', 'n_clicks')],
			 [State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date')])
def update_table(n_clicks, start_date, end_date):
    startDate = int(start_date[:10].replace("-",""))
    endDate = int(end_date[:10].replace("-","")) 
    start = dt.strptime(start_date, "%Y-%m-%d")
    end = dt.strptime(end_date, '%Y-%m-%d')
    start = int(start.strftime("%Y%m%d"))
    end = int(end.strftime("%Y%m%d"))

    conn = psycopg2.connect(
        database="newsLeader",
        user="postgres",
        password="Tianya1990",
        host="liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com",
        port='5432'
    )

    df = psql.read_sql("""SELECT * FROM public.news2020 WHERE "EventDateTime" BETWEEN %(dstart)s AND %(dfinish)s ORDER BY "ArticleCounts" DESC LIMIT 10;""", conn, params={"dstart":int(start),"dfinish":int(end)})
    df['EventDateTime'] = pd.to_datetime(df['EventDateTime'], format='%Y%m%d', errors='coerce')

    conn = None

    df.EventDateTime = pd.DatetimeIndex(df.EventDateTime).strftime("%Y-%m-%d")
    df = df.drop(columns=['IsRootEvent'])

    return generate_table(df, max_rows=10), generate_plot(df, max_rows=10),  generate_map(df, max_rows=10) 

if __name__ == '__main__':
    app.run_server(debug=True, port = 8060, host='ec2-35-171-44-44.compute-1.amazonaws.com')
    #app.run_server(debug=True)
