# %% [markdown]
# #### Functions (IGNORE for Readability)

# %%
# import packages that will be used for analysis
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import plotly.graph_objects as go
from dash import dcc,html,Output,Input
import dash

# %% [markdown]
# ##### Get Stock Data

# %%
missing_data_tickers = [] # use this as a list of tickers with missing data

def get_data_from_start_to_end(ticker, start_date, end_date):
    global missing_data_tickers  # Use the global list to accumulate missing tickers
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            missing_data_tickers.append(ticker)
            raise ValueError(f"Stock data for ticker {ticker} during the period from {start_date} to {end_date} was not found.")
        return stock_data
    except Exception as e:
        print(f"An error occurred for ticker {ticker}: {e}")
        missing_data_tickers.append(ticker)
        return None


# %%
# for a variety of periods load in different list of tickers
def download_stock_data_for_periods(tickers, periods):
    all_data = {}
    
    for period, (start_date, end_date) in periods.items():
        period_data = {}
        for ticker in tickers:
            data = get_data_from_start_to_end(ticker, start_date, end_date)
            if data is not None:
                period_data[ticker] = data
        all_data[period] = period_data
    
    return all_data

# %%
import pandas as pd

# Get the adjusted close prices
adj_close_sector_etf = {}

# Create adjusted close price only listing of sector ETFs
def get_adjusted_closed_price(nested_dict, tickers, periods):
    for period in periods:
        stock_price_df = pd.DataFrame()  # Create a new DataFrame for each period
        for ticker in tickers:
            stock_price_df[ticker] = nested_dict[period][ticker]['Adj Close']
        
        adj_close_sector_etf[period] = stock_price_df  # Store the complete DataFrame for the period
    
    return adj_close_sector_etf

# %% [markdown]
# ##### Plot go graph

# %%
# reusable function to create a time series plot

def plot_time_series(data,title,x_label,y_label):
    figure=go.Figure()

    for col in data.columns:
        figure.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode='lines',
            name='col'
        ))

    figure.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
)

    return figure


# %% [markdown]
# # Buy and Hold Strategy
# The buy and hold investment approach is where an investor purchases stocks or other assets and holds onto them. The period of holding a stock depends on its current performance and projections on the overall movement of the data. This strategy does not look at volatility as a factor as is a popular approach taken by many passive investors as it is build off the assumptions that over time the movement of the stock market is positive. Many investors like the simplicity and reduction in stress of frequest trading.

# %% [markdown]
# ## Sector ETFs
# ETFs are exchange traded funds which are the representation of an accumulation of a variety of stocks. They will try to represent a particular variable such a sector etf. This is where the ETF will take a proportion of a variety sized stocks in one of the 11 GICS Sectors (see documentation) to understand the overall movement of the sector. This looks to mitigate the impact of an individual companies success in understanding a sector. Understading sector performance are important for investing and macroeconomics. For example during a downturn sectors such as healthcare and consumer staples remain strong or outperform most benchmarks as they remain in demand, these are referred to as defensive stocks.
# 
# Sector ETFs have only become widely available recently so their history does not go back much further than 2005.

# %% [markdown]
# ## Macroeconomic Cycle
# The business cycle represents the overall aggregate demand within an economy and is very important for investing and macroeconomic policy. It is essential for investing as when the economy is in an expansion (increase) then businesses are increasing profits which increase share value. However, if you think back to Covid-19 or the Global Financial Crises when the economy was in freefall the majority of stocks did not perform well due to decreased demand due to large unemployment rates. All of these systems are related so understanding the performance of the economy is essential for looking at investment strategies. 

# %% [markdown]
# ### Buy and Hold Strategies using Sector ETFs during different Macroecnomic Cycles
# - Long term buy and hold: When the buy and hold period stretches greater than 10 years the success of the investment is less dependent on the business cycle. This is because within a 10 year period there will have been a number of movements but the assumption is that there is an increase in market with time.
# 
# - Mid term buy and hold: The investment strategy that will be looked at here will be one where the hold period is between 6 months and 3 years. The sector ETFs do not have historical data going back decades so data will be looked at from 2005-2024. Where there was a number of macroeconomic cycles.

# %%
# create time periods for where this takes place
economic_cycle_periods = {

    "trough": ("2008-10-01", "2009-06-01"),
    "expansion": ("2012-01-01", "2015-01-01"),
    "peak": ("2019-06-01", "2020-02-01"),
    "contraction": ("2007-12-01", "2008-10-01"),
    'all_data': ('2005-01-01','2024-06-01')
}

economic_cycle_periods_list = ['trough','expansion','peak','contraction','all_data']

# %%
# create etf tickers for sectors
sector_etf_tickers = [
    'XLB', # materials sector
    'XLI', # industrials sector
    'XLF', # financials
    'XLK', # information technology
    'XLY', # consumer discretionary
    'XLP', # consumer staples
    'XLE', # energy
    'XLV', # healthcare
    'VOX', # communication services
    'XLU', # utilities
    'IYR' # real estate
    ]

# %% [markdown]
# ### Load in Sector ETF Data
# Using different macroeconomic cycles and different sector ETFs load in the data via nested dictionary. This is going to allow you to access all relevant candlestick data via both the cycle and the sector etf.

# %%
# use down_stock_data_for_periods to get the neccessary stock data to be stored in a nested dict
sector_etf_data = download_stock_data_for_periods(sector_etf_tickers,economic_cycle_periods)

# %%
# practice example - access technology (XLK) sector ETF during an expansion
sector_etf_data['expansion']['XLK']

# %% [markdown]
# ### Use of Data
# As this investment strategy is used for long term stock data price, the only relevant data is going to be the adjusted close. The adjusted close is used instead of close as it incorporates stock splits which can heavily impact the close price. As a result create a single dataframe where it looks at each sector etfs adjusted close price with different periods.

# %%
# using the function 'get_adjusted_closed_price' get the adjusted close data
sector_etf_adjusted_close = get_adjusted_closed_price(sector_etf_data,sector_etf_tickers,economic_cycle_periods_list)

# %%
# show the adjusted close price for all sector ETFs durign an expansion
sector_etf_adjusted_close['expansion']

# %%


# %% [markdown]
# 

# %%
# set up dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label('Economic Time Period'),
    dcc.Dropdown(
        id='first-dropdown',
        options=[{'label':period,'value':period} for period in economic_cycle_periods_list],
        value = 'all_data'
    ),
    dcc.Graph(id='sector-etf-graph') # create a graph placeholder
])

@app.callback(
    Output('sector-etf-graph','figure'),
    [Input('first-dropdown','value')]
)

def update_graph(selected_period):
    # get the data for the selected period
    filtered_data = sector_etf_adjusted_close[selected_period]

    # use the fig creation 'plot_time_series' to create a visualization
    fig = plot_time_series(filtered_data,f'{selected_period} Sector ETF Adjusted Close','Date','Sector ETF price')

    return fig

# display the app
if __name__ == '__main__':
    app.run_server(port=8052)

# %%



