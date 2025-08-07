#Importing Libraries
import pandas as pd
import plotly.graph_objects as go
import numpy as np  
import yfinance as yf
import streamlit as st
import ta
import datetime
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import filter_data  
from pages.utils.plotly_figure import close_chart
from pages.utils.plotly_figure import candlestick
from pages.utils.plotly_figure import RSI
from pages.utils.plotly_figure import Moving_average
from pages.utils.plotly_figure import MACD


# Setting the page configuration
st.set_page_config(
    page_title="Stock Analysis", 
    page_icon="📄",
    layout="wide")
# Title of the page
st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

# Get today's date for default end date
today = datetime.date.today()

# Input for stock ticker
with col1:
    ticker = st.text_input("Enter Stock Ticker", "AAPL")
# Input for start date
with col2:  
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
# Input for end date 
with col3:
    end_date = st.date_input("Choose Start Date", datetime.date(today.year, today.month, today.day))

st.subheader(f"Stock Data for {ticker} from {start_date} to {end_date}")
# Fetching stock data
stock = yf.Ticker(ticker)
st.write(stock.info['longBusinessSummary'])
st.write('**Sector:**', stock.info.get('sector'))
st.write('**Industry:**', stock.info.get('industry'))
st.write('**Full Time Employees:**', stock.info.get('fullTimeEmployees'))
st.write('**Website:**', stock.info.get('website'))

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market Cap', 'P/E Ratio', 'Beta', 'EPS', '52 Week Low'])
    df[''] = [
        stock.info.get('marketCap'),
        stock.info.get('trailingPE'),        # <-- Correct key
        stock.info.get('beta'),
        stock.info.get('trailingEps'),
        stock.info.get('fiftyTwoWeekLow')    # <-- Correct key for 52-week low
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df2 = pd.DataFrame(index=['Qucik Ratio', 'Revenue Per Share', 'Profit Margins', 'Debt To Equity', 'Return On Equity'])
    df2[''] = [
        stock.info.get('quickRatio'),
        stock.info.get('revenuePerShare'),
        stock.info.get('profitMargins'),
        stock.info.get('debtToEquity'),
        stock.info.get('returnOnEquity')
    ]
    fig_df2 = plotly_table(df2)
    st.plotly_chart(fig_df2, use_container_width=True)


# Data Download
data = yf.download(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)

# Daily Change Calculation
daily_change = data['Close'][ticker.split()[0]].pct_change().dropna()
col1.metric("Daily Change", f"{daily_change.mean() * 100:.2f}%", f"{daily_change.std() * 100:.2f}%")

# Display Last 10 Days of Historical Data
last_10_days_data = data.tail(10).sort_index(ascending=False).round(3)
fig_df3 = plotly_table(last_10_days_data)
st.write("### Historical Data Last 10 Days ")
st.plotly_chart(fig_df3, use_container_width=True)

# Download Period Buttons
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1]*12)

num_period = ''
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('3M'):
        num_period = '3mo'
with col4:
    if st.button('6M'):
        num_period = '6mo'
with col5:
    if st.button('1Y'):
        num_period = '1y'
with col6:
    if st.button('2Y'):
        num_period = '2y'
with col7:
    if st.button('5Y'):
        num_period = '5y'
with col8:
    if st.button('10Y'):
        num_period = '10y'
with col9:
    if st.button('Max'):
        num_period = 'max'


col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox("Select Chart Type", ["Line", "Candlestick"])
with col2:
    if chart_type == "Candlestick":
       indicator = st.selectbox("Select Indicator", ["MACD", "RSI"])
    else:
        indicator = st.selectbox("Select Indicator", ["RSI", "Moving Average", "MACD"])


# Use selected period from buttons
ticker_ = yf.Ticker(ticker)
#period_used = num_period if num_period != '' else '1y'
if num_period != '':
    period_used = num_period
else:
    period_used = '1y'

data1 = ticker_.history(period=period_used)

# Chart rendering
if chart_type == "Candlestick" and indicator == "RSI":
    st.plotly_chart(candlestick(data1, period_used), use_container_width=True)

if chart_type == "Candlestick" and indicator == 'MACD':
    st.plotly_chart(candlestick(data1, period_used), use_container_width=True)
    st.plotly_chart(MACD(data1, period_used), use_container_width=True)

if chart_type == 'Line' and indicator == 'RSI':
    st.plotly_chart(close_chart(data1, period_used), use_container_width=True)
    st.plotly_chart(RSI(data1, period_used), use_container_width=True)

if chart_type == 'Line' and indicator == 'Moving Average':
    st.plotly_chart(close_chart(data1, period_used), use_container_width=True)
    st.plotly_chart(Moving_average(data1, period_used), use_container_width=True)

if chart_type == 'Line' and indicator == 'MACD':
    st.plotly_chart(close_chart(data1, period_used), use_container_width=True)
    st.plotly_chart(MACD(data1, period_used), use_container_width=True)
