import streamlit as st
import pandas as pd
import datetime
import pandas_datareader.data as web
import altair as alt

pd.options.display.float_format = '{:.2%}'.format

st.title("Delta portfolio")


#Sidebar
options = ["0A0H.UK", "COIN", "INTU", "TENB", "DASH", "XM", "AFRM", "BEIJ-B"]
selected_options = st.sidebar.multiselect('Which app do you want?',options)

# option = st.sidebar.multiselect('Select one or more symbols', ("0A0H.UK", "COIN", "INTU", "TENB", "DASH"))
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
tickers = ["0A0H.UK", "COIN", "INTU", "TENB", "DASH", "XM", "AFRM", "BEIJ-B"]


for ticker in tickers:
    df = web.DataReader(ticker, 'stooq', start_date, end_date)
    df["Ticker"] = ticker
    stockdata.append(df)

stockdata = pd.concat(stockdata)
stockdata = stockdata.sort_index(ascending=False)


stockdata_filtered = stockdata[stockdata["Ticker"].isin(selected_options)]
# stockdata_filtered = stockdata[stockdata["Ticker"]==[option]]
stockdata_filtered = stockdata_filtered.pivot(columns="Ticker", values="Close")
stockdata_filtered_pct_change = stockdata_filtered.pct_change(-1)
stockdata_filtered_pct_change = stockdata_filtered_pct_change.sort_index(ascending=False)
stockdata_filtered = stockdata_filtered.sort_index(ascending=False)

# cumprod
stockdata_filtered_pct_change_cumulative = (1 + stockdata_filtered_pct_change).cumprod() - 1
# stockdata_filtered_pct_change_cumulative = stockdata_filtered_pct_change_cumulative.reset_index()


#visualize tables
stockdata_filtered_pct_change_cumulative
stockdata_filtered_pct_change
stockdata_filtered

#Graphs
st.write("Stock returns")
st.line_chart(stockdata_filtered)
st.line_chart(stockdata_filtered_pct_change)