import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
import psycopg2
import psycopg2.extras
import plotly.graph_objs as go

conn = psycopg2.connect(
    database="newsLeader",
    user="postgres",
    password="Tianya1990",
    host="liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com",
    port='5432'
)

cur = conn.cursor()

newsDf = cur.execute("""SELECT "MentionIdentifier", "NumofCitation" FROM public.news ORDER BY "NumofCitation" DESC LIMIT 10""")
rows = cur.fetchall()

df = pd.DataFrame(rows)

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
        html.H1(children='News Leaders: trace the most cited news articles')
    ]),

    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2020, 2, 7),
        initial_visible_month=dt(2020, 2, 6),
        end_date=dt(2019, 12, 25),
        start_date = dt(2019, 11, 25)
    ),
    
    html.Div([
        html.H4(children='Table view'),
        generate_table(df),
        dcc.Graph(
            id="graph-1",
            figure={
                "data": [
                    go.Bar(
                        x=df[0],
                        y=df[1],
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
        )
    ], style={'columnCount': 1,'width': '52%', 'align': 'center'}),
])

if __name__ == '__main__':
    #app.run_server(debug=True, port = 8060, host='ec2-35-171-44-44.compute-1.amazonaws.com')
    app.run_server(debug=True)
