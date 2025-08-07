import streamlit as st
import yfinance as yf
import pandas as pd
st.set_page_config(
                    page_title="Trading App",
                    page_icon= "📉" ,
                    layout="wide"
)
st.title("Trading Guide App📊")
st.header("We provide the Greatest platform for you to collect all information prior to investing in stocks.")


st.image(r"C:\Users\DELL\OneDrive\Documents\C 1\CAPM\pages\app.png")


st.markdown("## We provide the following services:")

st.markdown("**:one: Stock Information**")
st.write("Through this page, you can see all the information about stock.")

st.markdown("**:two: Stock Prediction**")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models. Use this tool to gain valuable insights into potential future stock performance and make informed investment decisions.")

st.markdown("**:three: CAPM Return**")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks asset based on its risk.")

st.markdown("**:four: CAPM Beta**")
st.write("Calculates Beta and Expected Return for Individual Stocks.")
