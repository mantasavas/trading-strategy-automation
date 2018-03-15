import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

class CandlesIndexes():

	def __init__(self, stock_data):
		self.date = stock_data['Date']
		self.high = stock_data['High']
		self.low = stock_data['Low']
		self.close = stock_data['Close']
		self.stock_data = stock_data


	def display_candle_bars(self):
		# Creates two subplots, with shared x axis
		fig, (self.ax1, self.ax2) = plt.subplots(nrows=2, sharex=True)
		
		# Tells that x axis would be for date and sets desired format
		self.ax1.xaxis_date()
		self.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		self.ax1.set_title("Tesla Stock Prices (TSLA) Daily")
		# How x ticks are rotated
		plt.xticks(rotation=45)

		# Describes candles: color, width etc.
		candle_ohlc = candlestick_ohlc(self.ax1, self.stock_data.values, width=.5, colorup='b', alpha =1)
		self.ax1.set_ylabel("Cost (USD)")



	def display_bollinger_indicator(self, dates, top_band, bottom_band, mid_band):
		self.ax1.plot(dates, top_band, 'r', label='Upper Band')
		self.ax1.plot(dates, bottom_band, 'g', label='Lower Band')
		self.ax1.plot(dates, mid_band, 'b', label='Middle Band')
		self.ax1.legend(loc='upper left')


	def display_adx_indicator(self, dates, avg_direction_index, pos_directional_index, neg_directional_index):
		self.ax2.plot(dates[27:], avg_direction_index, 'r', label='ADX')
		self.ax2.plot(dates[14:], pos_directional_index, 'g',  label='+DX')
		self.ax2.plot(dates[14:], neg_directional_index, 'b', label='-DX')
		self.ax2.legend(loc='upper left')
		self.ax2.set_ylabel("Trend")

	def display(self):	
		plt.tight_layout()
		self.ax2.grid()
		self.ax1.grid()
		self.ax2.xaxis_date()
		self.ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		plt.show()
