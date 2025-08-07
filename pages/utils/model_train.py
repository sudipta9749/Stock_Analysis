# Imports
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

#1 Function to fetch stock data
def get_data(ticker):
    stock_data = yf.download(ticker, start='2024-01-01')
    return stock_data[['Close']]

#2 Function to check for stationarity using ADF test
def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value

#3 Function to compute 7-day rolling mean
def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price

#4 Function to determine the order of differencing needed for stationarity
def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while True:
        if p_value > 0.05:
            d += 1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
        else:
            break
    return d

#5 Function to train ARIMA model
def fit_model(data, differencing_order):  
    model = ARIMA(data, order=(30,differencing_order,30))
    model_fit = model.fit()

    forecast_steps = 30
    forecast = model_fit.get_forecast(steps=forecast_steps)

    predictions = forecast.predicted_mean
    return predictions

#6 Function to evaluate the model
def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]
    
    predictions = fit_model(train_data, differencing_order)  # Assumes fit_model is defined elsewhere
    
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)


#7 Function to scale the close price data
def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler

#8 Function to inverse scale the data
# def inverse_scaling(scaler, scaled_data):
#     # If the input is a pandas Series or 1D array, reshape it
#     if len(scaled_data.shape) == 1:
#         scaled_data = scaled_data.reshape(-1, 1)
#     return scaler.inverse_transform(scaled_data)

def inverse_scaling(scaler, scaled_data):
    # If it's a pandas Series, convert to numpy array first
    if isinstance(scaled_data, pd.Series):
        scaled_data = scaled_data.values.reshape(-1, 1)
    elif isinstance(scaled_data, np.ndarray) and scaled_data.ndim == 1:
        scaled_data = scaled_data.reshape(-1, 1)

    return scaler.inverse_transform(scaled_data)



#9 Function to get forecast for the next 30 days
def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)  # Assumes fit_model is defined elsewhere

    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    
    return forecast_df

