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


	def display_candle_bars(self, graph_number=2, sharex_xaxis=True):
		# Creates two subplots, with shared x axis
		fig, (self.ax1, self.ax2) = plt.subplots(nrows= graph_number, sharex= sharex_xaxis)
		
		# Tells that x axis would be for date and sets desired format
		self.ax1.xaxis_date()
		self.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		self.ax1.set_title("Tesla Stock Prices (TSLA) Daily & Bollinger Bands")
		# How x ticks are rotated
		plt.xticks(rotation=45)

		# Describes candles: color, width etc.
		candle_ohlc = candlestick_ohlc(self.ax1, self.stock_data.values, width=.5, colorup='b', alpha =1)
		self.ax1.set_ylabel("Cost (USD)")



	def display_bollinger_indicator(self, dates, top_band, bottom_band, mid_band, u_name = 'Upper Band', l_name = 'Lower Band', m_name = 'Middle Band'):
		self.ax1.plot(dates, top_band, 'r', label = u_name)
		self.ax1.plot(dates, bottom_band, 'g', label= l_name)
		self.ax1.plot(dates, mid_band, 'b', label= m_name)
		self.ax1.legend(loc='upper left')


	def display_adx_indicator(self, dates, avg_direction_index, pos_directional_index, neg_directional_index):
		self.ax2.plot(dates[27:], avg_direction_index, 'r', label='ADX')
		self.ax2.plot(dates[14:], pos_directional_index, 'g',  label='+DX')
		self.ax2.plot(dates[14:], neg_directional_index, 'b', label='-DX')
		self.ax2.set_title("Average Directional Index (ADX)")
		self.ax2.legend(loc='upper left')
		self.ax2.set_ylabel("Trend")

	def display_indicators(self):	
		self.ax2.grid()
		self.ax1.grid()
		self.ax2.xaxis_date()
		self.ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		plt.tight_layout()
		plt.show()





	# Displays candle sticks of stock data, bollinger indicator, profit graph
	def display_strategy(self, bollinger_one, bollinger_two, date_borrowed, price_borrowed, date_returned, price_returned, date_profit, price_profit):
	

		#profit = price_borrowed - price_returned

		self.display_candle_bars()

		self.display_bollinger_indicator(bollinger_one.dates_band, bollinger_one.top_band, bollinger_one.bottom_band, bollinger_one.mid_band,
										 'Upper Band 1', 'Lowe Band 1', 'Middle Band 1')
		self.display_bollinger_indicator(bollinger_two.dates_band, bollinger_two.top_band, bollinger_two.bottom_band, bollinger_two.mid_band,
										 'Upper Band 2', 'Lowe Band 2', 'Middle Band 2')


		self.ax1.plot(date_borrowed, price_borrowed, linestyle = 'None', marker='o',  color='k')
		self.ax1.plot(date_returned, price_returned, linestyle = 'None', marker='x',  color='k')



		#self.ax2.bar(date_profit, price_profit, width=0.2, color='r')
		self.ax2.plot(date_profit, price_profit, color = 'r', label = 'Sell Profit')
		self.ax2.set_title("Mean Reversal Strategy")
		self.ax2.legend(loc='upper left')
		self.ax2.set_ylabel("Profit (USD)")


		self.ax2.grid()
		self.ax1.grid()
		self.ax2.xaxis_date()
		self.ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		plt.tight_layout()
		plt.show()
