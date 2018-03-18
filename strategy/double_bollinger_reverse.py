import collections
import numpy as np

class DoubleBollingerReverse:
	def __init__(self, candle, bollinger_one, bollinger_two):
		self.candle = candle
		self.bollinger_one = bollinger_one
		self.bollinger_two = bollinger_two

		self.deviation = len(self.candle.dates) - len(self.bollinger_one.dates_band)

		self.result = [0] * (self.deviation)
		
		self.borrowed_indicator = 0

		self.date_borrowed = []
		self.price_borrowed = []
		
		self.date_returned = []
		self.price_returned = []

		self.price_profit = []
		self.date_profit = []
		self.price_profit_total = [0]
		self.current_profit = 0


	def mean_reverse_sell(self):
	
		for index in range(self.deviation, len(self.candle.dates)):
	
			# Checks if candle values fall into upper bands of bollinger
			if (self.candle.low[index] >= self.bollinger_one.top_band[index - self.deviation]) and (self.candle.low[index] <= self.bollinger_two.top_band[index - self.deviation]):
				self.result.append(1)

			elif (self.candle.high[index] >= self.bollinger_one.top_band[index - self.deviation]) and (self.candle.high[index] <= self.bollinger_two.top_band[index - self.deviation]):
				self.result.append(1)

			elif (self.candle.high[index] >= self.bollinger_two.top_band[index - self.deviation]) and (self.candle.low[index] <= self.bollinger_one.top_band[index - self.deviation]):
				self.result.append(1)

			else:
				self.result.append(0)


			
			# 1 activation
			# 0 no action
			# -1 returned
			# 2 borrowed
			length = len(self.result)
			# Check if it's a perfect time to borrow some stocks
			if(self.result[length - 3] == 1 and self.candle.close[index - 2] > self.candle.close[index - 1] and self.candle.close[index - 1] > self.candle.close[index - 0]):
				
				# If it is, borrow

				# Have we already borrowed and candle low is above bollinger middle? If yess, don't borrow again, wait till we exit.
				if self.borrowed_indicator == 0 and self.candle.low[index] > self.bollinger_one.mid_band[index - self.deviation]:
					print("Inside yeeeeee!!")
					self.borrowed_indicator = 1
					self.result[length - 1] = 2

					self.date_borrowed.append(self.candle.dates[index])
					self.price_borrowed.append(self.candle.low[index])


			# If we did borrowed defining three exit points: 
			# 1) when we reached stop loss
			# 2) when we reached take price_profit
			# 3) when we reached middle band of bollinger

			# IF middle band crosses price bar take price of intersected place 
			if self.borrowed_indicator == 1 and self.bollinger_one.mid_band[index - self.deviation] <= self.candle.high[index] and self.bollinger_one.mid_band[index - self.deviation] >= self.candle.low[index]:
				self.borrowed_indicator = 0
				self.result[length - 1] = -1

				self.date_returned.append(self.bollinger_one.dates_band[index - self.deviation])
				self.price_returned.append(self.bollinger_one.mid_band[index - self.deviation])

				# Calculating total profit
				self.current_profit += self.price_borrowed[len(self.price_borrowed) - 1] - self.price_returned[len(self.price_returned) - 1]
				self.price_profit.append(self.current_profit)
				self.date_profit.append(self.candle.dates[index])
				#print(self.current_profit, self.candle.dates[index])
	
			# IF price bar openened bellow middle band, take open price
			elif self.borrowed_indicator == 1 and self.bollinger_one.mid_band[index - self.deviation] >= self.candle.open[index]:
				self.borrowed_indicator = 0
				self.result[length - 1] = -1

				self.date_returned.append(self.candle.dates[index])
				self.price_returned.append(self.candle.open[index])

				# Calculating total profit
				self.current_profit += self.price_borrowed[len(self.price_borrowed) - 1] - self.price_returned[len(self.price_returned) - 1]
				self.price_profit.append(self.current_profit)
				self.date_profit.append(self.candle.dates[index])
				#print(self.current_profit, self.candle.dates[index])

			# IF candle still dind't crossed middle band, take close price
			elif(self.borrowed_indicator == 1):
				profit = self.current_profit + (self.price_borrowed[-1] - self.candle.close[index])
				self.price_profit.append(profit)
				self.date_profit.append(self.candle.dates[index])

			else:
				self.price_profit.append(self.current_profit)
				self.date_profit.append(self.candle.dates[index])



		return self.date_borrowed, self.price_borrowed, self.date_returned, self.price_returned, self.date_profit, self.price_profit