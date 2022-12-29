from inspect import trace
from typing import Container
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash_html_components.Col import Col
from dash_html_components.Legend import Legend
from numpy.lib.function_base import place
from numpy.lib.nanfunctions import _divide_by_count
import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc




"""
Beijer
Coinbase
Intuit Inc
Tenable Holdings Inc
DoorDash Inc
Avanza Zero
"""


# external_stylesheets = [dbc.themes.BOOTSTRAP]
BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

#######
# What holdings do we have? Amounts, value
# What is our expected returns?
# What is our risk(standard deviation)
# What is our returns?
# What is our riskadjusted returns?
######


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[BS])
# What holdings do we have? Amounts, value
tickers = ["BEIA-B.ST", "COIN", "INTU", "TENB", "DASH", "^DJI"]

# holdings = {'Stock': 'Beijer Ref', 'amount': 2
#         {'Stock': 'Coinbase', 'amount':},
#         {'Stock': 'Inuit Inc', 'amount': },
#         {'Stock': 'Tenable Holdings', 'amount': },
#         {'Stock': 'Door Dash', 'amount': }

options = [
        {'label': 'Beijer Ref', 'value': "BEIA-B.ST"},
        {'label': 'Coinbase', 'value': "COIN"},
        {'label': 'Intuit Inc', 'value': "INTU"},
        {'label': 'Tenable Holdings', 'value': "TENB"},
        {'label': 'Door Dash', 'value': "DASH"},
        {'label': 'Dow Jones', 'value': "^DJI"}
    ]

start = dt.datetime(2021, 4, 15)
end = dt.datetime.now()

##STOCKDATA
stockdata = []

for ticker in tickers:
    df = web.DataReader(ticker, 'yahoo', start, end)
    df["Ticker"] = ticker
    stockdata.append(df)

stockdata = pd.concat(stockdata)
# stockdata = stockdata.sort_index(ascending=False)
stockdata = stockdata[["Adj Close", "Ticker"]]
stockdata.head()
##COPY DATAFRAME
stockdata2 = stockdata.copy()
stockdata2 = stockdata2[["Ticker", "Adj Close"]]
# stockdata2.head()
stockdata2 = stockdata2.reset_index()
stockdata2 = stockdata2.pivot_table(
    index = ["Date"],
    columns=["Ticker"],
    values=["Adj Close"],
    dropna=False)
stockdata2 = stockdata2.sort_index(ascending=True)
stockdata2.columns = stockdata2.columns.droplevel(0)

stockdata2.head()
# stockdata2.info()
## STOCK RETURN
stock_return = stockdata2.apply(lambda x: x / x[0])
# stock_return.head(5)

# stock_return = stock_return.rename_axis(None, axis="columns")
# stock_return = stock_return.rename_axis(None)
stock_return = stock_return.reset_index()
# stock_return.head(-50)
# stock_return.columns.nlevels
# stock_return = stock_return.set_index("Date")
# stock_return = stock_return.sort_index(ascending=False).head(3)
stock_return2 = pd.melt(stock_return, id_vars=["Date"], var_name = "Ticker", value_name="Adj Close",)
stock_return2 = stock_return2.sort_index(ascending=False)
# print(stock_return2.head())

# What is our expected returns?
# What is our risk(standard deviation)
# What is our returns?
# What is our riskadjusted returns?

app.layout = dbc.Container(
                [dbc.Row(                   
                        dbc.Col(
                        [
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H1("Delta Investment Club"),
                            dcc.Dropdown(
                                    id='dropdown',
                                    options=options,
                                    value=tickers,
                                    multi=True, 
                                    placeholder="Choose a stock", 
                                    clearable=False),
                            html.Br(),
                            html.Br(),
                        ]),
                ),
                dbc.Row([        
                        dbc.Col(
                        [   
                                html.H1("Stock price"),
                                dcc.Graph("fig")
                        ]),
                        dbc.Col(
                        [    
                                html.H1("Stock returns"),
                                dcc.Graph("fig2")
                            
                        ]),
                dbc.Row([
                    html.H2("Stock data"),
                    html.Br(),
                    html.Br(),
                    dash_table.DataTable(
                        id='table',
                        columns= [
            {'name': i, 'id': i} for i in stockdata2.columns
        ],
                        data=stockdata2.to_dict("Records"),
                    )]
                ),
                ])],
            )

@app.callback(
    Output('fig', 'figure'),
    Output("fig2", "figure"),
    [Input('dropdown', 'value')])

def update_figure(value):
    if value is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    
    df = stockdata.copy()
    # print(value)
    df_filtered = df[(df['Ticker'].isin(value))]
    # print(df_filtered.head())
    
    fig = px.line(df_filtered, y="Adj Close", color="Ticker")

# def update_figure2(value):
    df_returns = stock_return2.copy()
    # print(df_returns.head())
    df_returns_filtered = df_returns[(df_returns['Ticker'].isin(value))]
    # print(df_returns_filtered.head())   
    
    fig2 = px.line(df_returns_filtered, x="Date", y="Adj Close", color="Ticker")

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return [fig,fig2]

if __name__ == '__main__':
    app.run_server(debug=True)