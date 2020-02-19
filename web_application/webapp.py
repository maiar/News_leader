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

conn = psycopg2.connect(
    database="newsLeader",
    user="postgres",
    password="Tianya1990",
    host="liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com",
    port='5432'
)

df = psql.read_sql("""SELECT a.*, b.count FROM public.events a INNER JOIN (SELECT * FROM public.citations AS ranks ORDER BY "count" DESC LIMIT 10) b ON a."GlobalEventID" = b."GlobalEventID" ORDER BY "count" DESC;""", conn)
df['EventDateTime'] = pd.to_datetime(df['EventDateTime'], format='%Y%m%d', errors='coerce')
df.EventDateTime = pd.DatetimeIndex(df.EventDateTime).strftime("%Y-%m-%d")
#df.index = df['EventDateTime']

conn = None

print(df.columns)
print(df.dtypes)
print("\n")

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
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
            html.H4(children='Plot view'),
            dcc.Graph(
                id="bar-plot",
                figure={
                    "data": [
                        go.Bar(
                            x=df['Url'],
                            y=df['count'],
                            marker={
                                "color": "#97151c",
                                "line": {
                                    "color": "rgb(255, 255, 255)",
                                    "width": 2,
                                },
                            },
                            name="Calibre Index Fund",
                        ),
                    ], 
                },
            ),
            html.H4(children='Table view'),
            
            #html.Div(id='table')
            generate_table(df)
        ]),
    ], style={'width': '80%','margin': '0 auto', 'text-align': 'center'})   
], style={'margin': '0'}
)
'''
@app.callback(Output('table', 'children'),
			 [Input('button', 'n_clicks')],
			 [State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date')])
def update_graph(n_clicks, start_date, end_date):
    startDate = int(start_date[:10].replace("-",""))
    endDate = int(end_date[:10].replace("-","")) 
    print(startDate)
    print(endDate)
    print(type(start_date))
    print(type(end_date))
    start = dt.strptime(start_date, "%Y-%m-%d")
    end = dt.strptime(end_date, '%Y-%m-%d')
    print(start.strftime("%Y%m%d"))
    print(end.strftime("%Y%m%d"))

    conn = psycopg2.connect(
        database="newsLeader",
        user="postgres",
        password="Tianya1990",
        host="liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com",
        port='5432'
    )

    df = psql.read_sql("""SELECT a.*, b.count FROM public.events a INNER JOIN (SELECT * FROM public.citations AS ranks ORDER BY "count" DESC LIMIT 10) b ON a."GlobalEventID" = b."GlobalEventID" ORDER BY "count" DESC;""", conn)
    df['EventDateTime'] = pd.to_datetime(df['EventDateTime'], format='%Y%m%d', errors='coerce')
    #df.EventDateTime = pd.DatetimeIndex(df.EventDateTime).strftime("%Y-%m-%d")
    #df.index = df['EventDateTime']

    conn = None

    print(df.columns)
    print(df.dtypes)
    print("\n")
    #df2 = df.loc[start: end]
    #print(type(df2))

    df.EventDateTime = pd.DatetimeIndex(df.EventDateTime).strftime("%Y-%m-%d")
    # df2.EventDateTime = pd.DatetimeIndex(df2.EventDateTime).strftime("%Y-%m-%d")

    return generate_table(df, max_rows=10)
'''

if __name__ == '__main__':
    #app.run_server(debug=True, port = 8060, host='ec2-35-171-44-44.compute-1.amazonaws.com')
    app.run_server(debug=True)
