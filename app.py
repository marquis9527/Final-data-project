import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data_url = "https://raw.githubusercontent.com/NiuLearner/dashPython/main/Stocks.csv"
df_all = pd.read_csv(data_url)

available_tickers = df_all['Ticker'].unique()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Financial Dashboard"),
    
    html.Label("Select Stock Tickers:"),
    dcc.Checklist(
        id='ticker_checklist',
        options=[{'label': i, 'value': i} for i in available_tickers],
        value=available_tickers,  
    ),
    
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Stock Price', value='tab-1'),
        dcc.Tab(label='Stock Volume', value='tab-2'),
        dcc.Tab(label='Market Share', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('ticker_checklist', 'value')]
)
def update_tab(tab, selected_tickers):
    filtered_df = df_all[df_all['Ticker'].isin(selected_tickers)]
    
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(
                figure=px.line(
                    filtered_df, x='Date', y='Close',
                    color='Ticker', title='Stock Price Over Time'
                )
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                figure=px.bar(
                    filtered_df, x='Date', y='Volume',
                    color='Ticker', title='Stock Volume Over Time'
                )
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(
                figure=px.pie(
                    filtered_df.groupby('Ticker').agg({'Close': 'mean'}).reset_index(),
                    values='Close', names='Ticker', title='Market Share by Stock'
                )
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
