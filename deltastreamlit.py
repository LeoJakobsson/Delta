import streamlit as st
import pandas as pd
import datetime
import pandas_datareader.data as web
import altair as alt



st.title("Delta portfolio")


#Sidebar
option = st.sidebar.selectbox('Select one symbol', ("0A0H.UK", "COIN", "INTU", "TENB", "DASH"))
today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

#Stockdata
stockdata = []
tickers = ["0A0H.UK", "COIN", "INTU", "TENB", "DASH"]


for ticker in tickers:
    df = web.DataReader(ticker, 'stooq', start_date, end_date)
    df["Ticker"] = ticker
    stockdata.append(df)

stockdata = pd.concat(stockdata)
stockdata = stockdata.sort_index(ascending=False)

stockdata_filtered = stockdata[stockdata["Ticker"]==option]
stockdata_filtered

#Graphs
st.write("Stock returns")
st.line_chart(stockdata_filtered)