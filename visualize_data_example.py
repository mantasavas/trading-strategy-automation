import pandas as pd
from pandas.compat import StringIO
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import average_directional_index as adx
import numpy as np
import time





# Calculate standart deviation for given interval (ex. 10 days)
# Interval_length - size of interval
# Closed - candle prices (not open, neither max or min)
# Dates - dates of prices closed
def standart_deviation(interval_length, prices, dates):
    stand_deviation = []
    date = []
    x = interval_length

    while x < len(prices):
        interval_prices = prices[x - interval_length : x]
        std_calculated = interval_prices.std()
        stand_deviation.append(std_calculated)
        date.append(dates[x])
        x += 1

    return stand_deviation, date






#https://stackoverflow.com/questions/20036663/understanding-numpys-convolve
def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    #print(weights)
    return smas # as a numpy array
    





# Function for calculating bollinger indicator
# Middle band formula: (time_diff)SMA
# Top band formula: (time_diff)SMA + (time_diff)standart_deviation * multiplier(usually by 2)
# Bottom band formula: (time_diff)SMA - (time_diff)standart_deviation * multiplier(usually by 2)
def bollinger_bands(multiplier, time_diff, date, closed_price):
    top_band = []
    bottom_band = []
    mid_band = []
    dates_band = []

    x = time_diff

    # Calculating standart deviation of all periods
    standart_dev, dates_band = standart_deviation(time_diff, closed_price, date)
   
    # Calculating bands of all periods
    while x < len(date):
        # We want only the last element so -1, 
        simple_moving_avg = moving_average(closed_price[x-time_diff:x], time_diff)[-1]

        TB = simple_moving_avg + (standart_dev[x - time_diff] * multiplier)
        BB = simple_moving_avg - (standart_dev[x - time_diff] * multiplier)

        top_band.append(TB)
        bottom_band.append(BB)
        mid_band.append(simple_moving_avg)
        x += 1

    return top_band, bottom_band, mid_band, dates_band






# Plotting graph
def plot_candlestick(df):
    fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
    idx_name = df.index.name
    
    # Drops index and sets it as a column, and leaves only useful columns
    dat = df.reset_index()[[idx_name, "Open", "High", "Low", "Close"]]

    # Makes conversation between date and num
    dat[df.index.name] = dat[df.index.name].map(mdates.date2num)

    # Tells that x axis would be for date and sets desired format
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.set_title("Tesla Stock Prices (TSLA) Daily")
    # How x ticks are rotated
    plt.xticks(rotation=45)

    # Describes candles: color, width etc.
    candle_ohlc = candlestick_ohlc(ax, dat.values, width=.5, colorup='b', alpha =1)
    ax.set_ylabel("Cost (USD)")

    return ax, ax2




# Reading csv (comma seprated value) using panda dataframe
df = pd.read_csv("tesla_stock_data.csv", index_col='Date', parse_dates=True)

# Retrieving parameters required for calculating 10 days deviation
prices_data = df.loc[:, "Close"]
dates = df.index


top_band, bottom_band, mid_band, dates_band = bollinger_bands(2, 20, dates, prices_data)


ax, ax2 = plot_candlestick(df)
ax.plot(dates_band, top_band, 'r', label='Upper Band')
ax.plot(dates_band, bottom_band, 'g', label='Lower Band')
ax.plot(dates_band, mid_band, 'b', label='Middle Band')
ax.legend(loc='upper left')



pos_directional_index, neg_directional_index, avg_direction_index = adx.run_average_direction()
#print(pos_directional_index)
#print(neg_directional_index)
#print(avg_direction_index)

print(len(dates) - len(pos_directional_index))
print(len(dates) - len(avg_direction_index))
ax2.plot(dates[27:], avg_direction_index, 'r', label='ADX')
ax2.plot(dates[14:], pos_directional_index, 'g',  label='+DX')
ax2.plot(dates[14:], neg_directional_index, 'b', label='-DX')
ax2.legend(loc='upper left')
ax2.set_ylabel("Trend")


plt.tight_layout()
plt.show()







# Prints all columns from excel file
#print(answer.columns)