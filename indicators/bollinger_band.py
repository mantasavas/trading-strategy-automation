
import numpy as np

class BollingerIndicator:

	def __init__(self, dates, close, deviation, interval):
		self.dates = dates
		self.close = close
		self.deviation = deviation
		self.interval = interval

		self.top_band = []
		self.bottom_band = []
		self.mid_band = []
		self.dates_band = []
		

	# Calculate standart deviation for given interval (ex. 10 days)
	# Interval_length - size of interval
	# Closed - candle prices (not open, neither max or min)
	# Dates - dates of prices closed
	def standart_deviation(self, interval_length, prices, dates):
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
	def moving_average(self, values, window):
	    weights = np.repeat(1.0, window) / window
	    smas = np.convolve(values, weights, 'valid')
	    return smas
	    



	# Function for calculating bollinger indicator
	# Middle band formula: (time_diff)SMA
	# Top band formula: (time_diff)SMA + (time_diff)standart_deviation * multiplier(usually by 2)
	# Bottom band formula: (time_diff)SMA - (time_diff)standart_deviation * multiplier(usually by 2)
	def bollinger_bands(self):
		self.top_band = []
		self.bottom_band = []
		self.mid_band = []
		self.dates_band = []
		
		x = self.interval

	    # Calculating standart deviation of all periods
		standart_dev, self.dates_band = self.standart_deviation(self.interval, self.close, self.dates)
	   
	    # Calculating bands of all periods
		while x < len(self.dates):
	        # We want only the last element so -1, 
			simple_moving_avg = self.moving_average(self.close[x-self.interval:x], self.interval)[-1]

			TB = simple_moving_avg + (standart_dev[x - self.interval] * self.deviation)
			BB = simple_moving_avg - (standart_dev[x - self.interval] * self.deviation)

			self.top_band.append(TB)
			self.bottom_band.append(BB)
			self.mid_band.append(simple_moving_avg)
			x += 1
		
		return self.top_band, self.bottom_band, self.mid_band, self.dates_band


