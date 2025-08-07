# Importing Libraries
import pandas as pd
import pandas_datareader.data as web
import numpy as np  
import yfinance as yf
import streamlit as st
import datetime
import CAPM_FUNCTIONS as capm
#from datetime import date
st.set_page_config(
                    page_title="CAPM Return Calculator",
                    page_icon="📈", # "Chart With Upward Trends"
                    layout="wide"
)

st.title("Capital Asset Pricing Model")
col1,col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 Stocks",
               options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "BRK-B", "V","AFL"],
               default=["AAPL", "TSLA", "GOOGL", "AMZN"])
with col2:
    year = st.number_input("Enter Number of  Years", 
                min_value=1, 
                max_value=10)
    
# Download Data For SP500
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
    SP500 = web.DataReader(['sp500'],'fred', start, end)

    stock_df = pd.DataFrame()

    for stock in stocks_list:
        # Download Data For Stocks
        stock_data = yf.download(stock, period=f"{year}y")
        stock_df[stock] = stock_data['Close']
        # stock_data = stock_data['Adj Close']
        # stock_data = stock_data.to_frame(name=stock)
    stock_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)

    SP500 = SP500.rename(columns={'DATE': 'Date'}) # Renaming column for merging

    # Merging Data
    stock_df = pd.merge(stock_df, SP500, on='Date', how='inner')
    # print(stock_df)

    # Now we want to show first 500 and last 500 rows of the dataframe
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stock_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stock_df.tail(), use_container_width=True)

    # Plotting Interactive Charts
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all stocks")
        st.plotly_chart(capm.plot_interactive_charts(stock_df), use_container_width=True)
    with col2:
        st.markdown("### Normalized Price of all stocks")
        normalized_df = capm.normalize_prices(stock_df)  # Normalize prices
        st.plotly_chart(capm.plot_interactive_charts(normalized_df), use_container_width=True) # Again send to the interactive chart function for plotting
        # or
        #st.plotly_chart(capm.plot_interactive_charts(capm.normalize_prices(stock_df)), use_container_width=True)

    # Displaying Daily Returns
    stocks_daily_returns = capm.calculate_daily_returns(stock_df)  # Calculate daily returns
    st.markdown("### Daily Returns of Selected Stocks") 
    st.dataframe(stocks_daily_returns, use_container_width=True)
    # print(stocks_daily_returns)

    # Calculating Beta Values
    beta_values = {}
    alpha_values = {}
    for i in stocks_daily_returns:
        if i != 'Date' and i != 'sp500':
            beta = capm.calculate_beta(stocks_daily_returns[i], stocks_daily_returns['sp500'])
            beta_values[i] = float(beta)
            alpha = stocks_daily_returns[i].mean() - beta * stocks_daily_returns['sp500'].mean()
            alpha_values[i] = float(alpha) # Here use float to convert Series to scalar for display
    # print(beta_values, alpha_values)

    # Displaying Beta Values
    beta_df = pd.DataFrame.from_dict(beta_values, orient='index', columns=['Beta'])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Beta Values of Selected Stocks")
        st.dataframe(beta_df, use_container_width=True)
    # Calculating returns using CAPM formula
    risk_free_rate = 0.02  # Example risk-free rate, can be adjusted
    market_return = stocks_daily_returns['sp500'].mean() * 252  # Annualized market return
    capm_returns = {}
        
    for stock in beta_values:
        capm_return = risk_free_rate + beta_values[stock] * (market_return - risk_free_rate)
        capm_returns[stock] = capm_return    
        capm_returns_df = pd.DataFrame.from_dict(capm_returns, orient='index', columns=['Expected Return'])

    with col2:
        st.markdown("### Expected Returns using CAPM")
        st.dataframe(capm_returns_df, use_container_width=True)

except:
    st.write("An error occurred while fetching the data. Please check your inputs and try again.")

