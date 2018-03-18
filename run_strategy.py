from pandas.compat import StringIO
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import collections
import numpy as np
import time

# Display my data
from graphs import candles_indexes

# Average directional index
from indicators import bollinger_band
from indicators import adx

# Import my strategy
from strategy import double_bollinger_reverse

def display_graphs():
    deviation = 2
    moving_average = 20 

    # ============ Reading from file and formatting ============

    # Reading csv (comma seprated value) using panda dataframe and potting
    stock_info = pd.read_csv("./files/tesla_stock_data.csv", index_col='Date', parse_dates=True)

    # Retrieving parameters required for adx and bollinger bands
    high = stock_info.loc[:, "High"]
    low = stock_info.loc[:, "Low"]
    close = stock_info.loc[:, "Close"]
    dates = stock_info.index

     # Drops index and sets it as a column, and leaves only useful columns
    stock_data = stock_info.reset_index()[[dates.name, "Open", "High", "Low", "Close"]]
    stock_data[dates.name] = stock_data[dates.name].map(mdates.date2num)

    CandleStick = collections.namedtuple('CandleStick', 'dates open high low close')
    candle = CandleStick(dates = dates, open = stock_data['Open'], high = stock_data['High'], low = stock_data['Low'], close = stock_data['Close'])

    # ============ Calculating Indicators ==============
    
    Bollinger = collections.namedtuple("Bollinger", 'dates_band top_band bottom_band mid_band deviation moving_average') 


    bollinger_ind = bollinger_band.BollingerIndicator(dates, close, 2, 20)
    top_band, bottom_band, mid_band, dates_band = bollinger_ind.bollinger_bands()
    bollinger_one =  Bollinger(dates_band = dates_band, top_band = top_band, bottom_band = bottom_band, mid_band = mid_band, deviation=deviation, moving_average = moving_average)

    bollinger_ind.deviation = 3;
    top_band, bottom_band, mid_band, dates_band = bollinger_ind.bollinger_bands()
    bollinger_two = Bollinger(dates_band = dates_band, top_band = top_band, bottom_band = bottom_band, mid_band = mid_band, deviation = deviation, moving_average = moving_average)



    # ============ Calculating Strategy ==============
    
    bollinger_reverse = double_bollinger_reverse.DoubleBollingerReverse(candle, bollinger_one, bollinger_two)
    date_borrowed, price_borrowed, date_returned, price_returned, date_profit, price_profit = bollinger_reverse.mean_reverse_sell()
    


    # ============ Displaying Indicators ==============
    
    
    candles = candles_indexes.CandlesIndexes(stock_data)
    candles.display_strategy(bollinger_one, bollinger_two, date_borrowed, price_borrowed, date_returned, price_returned, date_profit, price_profit)





if __name__ == "__main__":
    display_graphs()
