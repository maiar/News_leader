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

newsDf = cur.execute("""SELECT "MentionIdentifier", "count" FROM public.citations ORDER BY "count" DESC LIMIT 10""")
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
            html.Img(
            src=app.get_asset_url('frontend.png'),
            style={'width': '100%', 'margin': '0'}
        ),
    ]),

    html.Div([
        html.Div([
            html.H1(children='News Leaders: trace the most cited news articles')
        ]),

        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=dt(1995, 8, 5),
                max_date_allowed=dt(2020, 2, 7),
                initial_visible_month=dt(2020, 2, 6),
                end_date=dt(2019, 12, 25),
                start_date = dt(2019, 11, 25),
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
            ),
            html.H4(children='Table view'),
            generate_table(df)        
        ]),
    ], style={'width': '54%','margin': '0 auto', 'text-align': 'center'})   
], style={'margin': '0'}
)

'''
@app.callback(
    dash.dependencies.Output('bar-plot', 'selectedData'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('date-picker-range', 'start_date')])
def update_output(n_clicks, start_date):
    string_prefix = 'You have selected: '
    if date is not None:
        date = dt.strptime(date.split(' ')[0], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        return string_prefix + date_string
    print(string_prefix+date_string)
'''

if __name__ == '__main__':
    #app.run_server(debug=True, port = 8060, host='ec2-35-171-44-44.compute-1.amazonaws.com')
    app.run_server(debug=True)
