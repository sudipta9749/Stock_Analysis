# Import necessary libraries
import plotly.graph_objects as go
import streamlit as st
import datetime
import dateutil


#1 Function to create a Plotly table from a DataFrame
# This function takes a DataFrame and returns a Plotly figure object
def plotly_table(dataframe, *args, **kwargs):
    headerColor = '#0078ff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ["<b>" + str(col)[:10] + "</b>" for col in dataframe.columns],
            line_color=headerColor,
            fill_color=headerColor,
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[[f"<b>{i}</b>" for i in dataframe.index]] +
                   [dataframe[col].tolist() for col in dataframe.columns],
            fill_color='lavender',
            align='left',
            font=dict(color="black", size=15),
            line_color='white'
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

#2 Function to filter data based on a specified period
# This function takes a DataFrame and a period string, and returns a filtered DataFrame
def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)

    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)

    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
        
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)

    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)

    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1,1).strftime('%Y-%m-%d')

    else:
        date = dataframe.index [0]

    return dataframe.reset_index() [dataframe.reset_index() ['Date']>date]

#3 Function to close a chart with specified data and period
# This function takes a DataFrame and a period string, and returns a Plotly figure object
def close_chart(dataframe, num_period =False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], 
                        mode='lines',
                        name='Open', line = dict(width=2,color = '#5ab7ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], 
                        mode='lines', 
                        name='Close', line = dict(width=2,color = 'black')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe ['High'],
                        mode='lines', 
                        name='High', line= dict(width=2, color = '#0078ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], 
                        mode='lines', 
                        name='Low', line = dict(width=2,color='red')))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',  # light blue-gray (example)
        # legend=dict(
        # yanchor="top",
        # xanchor="right",
        legend=dict(
            yanchor="top",
            xanchor="right",
            font=dict(
                color="blue",    # Set legend text color here
                size=12          # Optional: control font size
            )
    ))
    return fig

#4 Function to create a candlestick chart
# This function takes a DataFrame and a period string, and returns a Plotly figure object
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=dataframe ['Date'],
    open = dataframe['Open'], high = dataframe['High'],
    low = dataframe['Low'], close = dataframe['Close']))

    fig.update_layout (
        showlegend = False, 
        height = 500, 
        margin = dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor= 'white', 
        paper_bgcolor='#e1efff'  # ✅ VALID HEX COLOR
)

    return fig
# def candlestick(dataframe, num_period):
#     dataframe = filter_data(dataframe, num_period)
#     fig = go.Figure()

#     fig.add_trace(go.Candlestick(
#         x=dataframe['Date'],
#         open=dataframe['Open'],
#         high=dataframe['High'],
#         low=dataframe['Low'],
#         close=dataframe['Close'],
#         name='Candlestick'  # ✅ Added name for legend
#     ))

#     fig.update_layout(
#         showlegend=True,  # ✅ Enable legend
#         height=500,
#         margin=dict(l=0, r=20, t=20, b=0),
#         plot_bgcolor='white',
#         paper_bgcolor='#e1efff'
#     )

#     return fig


#5 Function to calculate RSI (Relative Strength Index)
# This function takes a DataFrame and a period string, and returns a Plotly figure object
def RSI(data, duration='1y', num_period=14):
    data = data.copy()

    # Resample data to daily to ensure fixed frequency
    data = data.asfreq('D')  # Set to daily frequency
    data = data.fillna(method='ffill')  # Fill missing days (weekends, holidays)

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=num_period, min_periods=num_period).mean()
    avg_loss = loss.rolling(window=num_period, min_periods=num_period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data['RSI'] = rsi

    # Filter based on duration
    if duration == '1y':
        data = data.last('365D')
    elif duration == '6mo':
        data = data.last('180D')
    elif duration == '3mo':
        data = data.last('90D')
    elif duration == '1mo':
        data = data.last('30D')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI')
    return fig



#6 Function to calculate Moving Average
# This function takes a DataFrame and a period string, and returns a Plotly figure object
def Moving_average(dataframe, num_period):
    # Calculate SMA manually using pandas
    dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()

    # Assuming you have this function to filter the dataframe
    dataframe = filter_data(dataframe, num_period)

    # Create the plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines', name='Close', line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode='lines', name='High', line=dict(width=2, color='#0078ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode='lines', name='Low', line=dict(width=2, color='red')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines', name='SMA 50', line=dict(width=2, color='purple')
    ))

    # Customize the layout
    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',  # light bluish color
        legend=dict(
            yanchor="top",
            xanchor="right",
            font=dict(
                color="blue",    # Set legend text color here
                size=12          # Optional: control font size
            )
        )
    )

    return fig


#7 Function to calculate MACD (Moving Average Convergence Divergence)
# This function takes a DataFrame and a period string, and returns a Plotly figure object
def MACD(dataframe, num_period):
    short_ema = dataframe['Close'].ewm(span=12, adjust=False).mean()
    long_ema = dataframe['Close'].ewm(span=26, adjust=False).mean()
    
    macd = short_ema - long_ema
    macd_signal = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - macd_signal

    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist

    # Assuming filter_data is already defined
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='RSI',
        marker_color='orange',
        line=dict(width=2, color='orange'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='Overbought',
        marker_color='red',
        line=dict(width=2, color='red', dash="dash"),
    ))

    c = ['red' if cl < 0 else 'green' for cl in macd_hist]
    
    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top", y=1.82, xanchor="right", x=1)
    )
    
    return fig

