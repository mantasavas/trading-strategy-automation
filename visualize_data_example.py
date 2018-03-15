from pandas.compat import StringIO
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import time

# Display data
from graphs import candles_indexes

# Average directional index
from indicators import bollinger_band
from indicators import adx


def display_graphs():
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


    # ============ Calculating Indicators ==============
    bollinger_ind = bollinger_band.BollingerIndicator(dates, close, 2, 20)
    top_band, bottom_band, mid_band, dates_band = bollinger_ind.bollinger_bands()

    adx_index = adx.AverageDirectionalIndex(high, low, close)
    pos_directional_index, neg_directional_index, avg_direction_index = adx_index.run_average_direction()


    # ============ Displaying Indicators ==============
    candles = candles_indexes.CandlesIndexes(stock_data)
    candles.display_candle_bars()
    
    candles.display_bollinger_indicator(dates_band, top_band, bottom_band, mid_band)
    candles.display_adx_indicator(dates, avg_direction_index, pos_directional_index, neg_directional_index)

    candles.display()


if __name__ == "__main__":
    display_graphs()
