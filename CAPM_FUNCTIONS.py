# Importing necessary libraries
import plotly.express as px

# Function to plot the interactive charts
def plot_interactive_charts(stock_df):
    # Melt the DataFrame to have a long format for plotting
    melted_df = stock_df.melt(id_vars=['Date'], var_name='Stock', value_name='Price')

    # Create an interactive line chart using Plotly Express
    fig = px.line(melted_df, x='Date', y='Price', color='Stock', title='Stock Prices Over Time')
    
    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Stocks',
        template='plotly_white'
    )
    
    return fig


# Function to normalize the prices based on the initial price
def normalize_prices(stock_df):
    # Normalize the prices to the first row for each stock
    normalized_df = stock_df.copy()
    for stock in stock_df.columns[1:]:  # Skip the 'Date' column
        normalized_df[stock] = normalized_df[stock] / normalized_df[stock].iloc[0]
    
    return normalized_df

# Function to calculate daily returns
def calculate_daily_returns(stock_df):
    # Calculate daily returns for each stock
    returns_df = stock_df.copy()
    for stock in stock_df.columns[1:]:  # Skip the 'Date' column
        returns_df[stock] = returns_df[stock].pct_change()
    
    # Drop the first row with NaN values after pct_change
    returns_df.dropna(inplace=True)
    
    return returns_df

# Function to calculate beta values
def calculate_beta(stock_returns, market_returns):
    # Calculate covariance between stock returns and market returns
    covariance = stock_returns.cov(market_returns)
    
    # Calculate variance of market returns
    market_variance = market_returns.var()
    
    # Calculate beta
    beta = covariance / market_variance
    
    return beta