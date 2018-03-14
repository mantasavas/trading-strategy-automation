import numpy as np
import pandas as pd

file = pd.read_excel('test_data.xls')

'''
test_high = file['High'].values
test_low = file['Low'].values
test_close = file['Close'].values
'''

df = pd.read_csv("tesla_stock_data.csv", index_col='Date', parse_dates=True)
test_high = df.loc[:, "High"]
test_low = df.loc[:, "Low"]
test_close = df.loc[:, "Close"]




true_range = []
plus_directional_mov = []
nega_directional_mov = []
true_range_smoothed = []
plus_directional_mov_smoothed = []
nega_directional_mov_smoothed = []
pos_directional_index = []
neg_directional_index = []
directional_movement_index = []
avg_direction_index = []



# Accepted
# Calculates true range index
def true_range_calculate(high, low, yestarday_close):
	hl_diff = high - low
	h_yc = abs(high - yestarday_close)
	l_yc = abs(low - yestarday_close)

	# Picks the biggest out of three
	if h_yc <= hl_diff >= l_yc:
		true_range = hl_diff
	elif hl_diff <= h_yc >= l_yc:
		true_range = h_yc
	elif hl_diff <= l_yc >= h_yc:
		true_range = l_yc

	# Returns the biggest
	return true_range


# Finds directional movement if it's positive or negative
# Good example
def directional_movement(tod_high, tod_low, yest_high, yest_low):
	moveUp = tod_high - yest_high
	moveDown = yest_low - tod_low

	if 0 < moveUp > moveDown:
		positive_directional_mov = moveUp
	else:
		positive_directional_mov = 0


	if 0 < moveDown > moveUp:
		negative_directional_mov = moveDown
	else:
		negative_directional_mov = 0

	return negative_directional_mov, positive_directional_mov



ind = 1
while ind < len(test_high):
    # calculating true range
    # true_range_calculate(high, low, yestarday_close):
    true_range.append(true_range_calculate(test_high[ind], test_low[ind], test_close[ind - 1]))

    # calculating derectional moving, positive and negative
    # directional_movement(tod_high, tod_low, yest_high, yest_low)
    ng_dir_mov, pl_dir_mov = directional_movement(test_high[ind], test_low[ind], test_high[ind - 1], test_low[ind - 1])
    plus_directional_mov.append(pl_dir_mov)
    nega_directional_mov.append(ng_dir_mov)

    ind += 1; 



# Wilder's Smoothing Technique
# Smooth each period's +DM1, -DM1, and TR1 values over 14 periods
# First value simply sum of the firs 14 periods
def moving_wilder_smoothing(moving_values):
    smoothed_moving_values = []
    smoothed_moving_values.append(sum(moving_values[:14]))

    ind = 14;
    while(ind < len(moving_values)):
        previous_smoothed_mov_value = smoothed_moving_values[ind - 14]
        current_moving_value = moving_values[ind]

        #print(previous_smoothed_true_range, current_true_range)

        current_smoothed_mov_value = previous_smoothed_mov_value - (previous_smoothed_mov_value / 14) + current_moving_value
        smoothed_moving_values.append(current_smoothed_mov_value)
        ind += 1 
    return smoothed_moving_values


# Calculates +DI and -DI requered for plotting
def find_directional_index(smoothed_true_range, pos_directional_mov, neg_directional_mov):
    pos_dir_ind = []
    neg_dir_ind = []
    directional_index = []

    for ind in range(0, len(smoothed_true_range)):
        pos_dir_ind.append((pos_directional_mov[ind] / smoothed_true_range[ind] ) * 100)
        neg_dir_ind.append(( neg_directional_mov[ind] / smoothed_true_range[ind] ) * 100)
        diff_ind = abs(pos_dir_ind[ind] - neg_dir_ind[ind])
        sum_ind = pos_dir_ind[ind] + neg_dir_ind[ind];
        directional_index.append(( diff_ind / sum_ind ) * 100)

    return pos_dir_ind, neg_dir_ind, directional_index


# Average directional index calculation
def average_directional_index(directional_movement_index):
    avg_direct_index = []
    avg_direct_index.append(np.mean(directional_movement_index[:14]))
    
    for ind in range(14, len(directional_movement_index)):
        avg_direct_index.append((avg_direct_index[ind - 14] * 13 + directional_movement_index[ind]) / 14)
    return avg_direct_index



def run_average_direction():
	# Calculating true range smooved values
	true_range_smoothed = moving_wilder_smoothing(true_range)

	# Calculating +DM1 smoothed values
	plus_directional_mov_smoothed = moving_wilder_smoothing(plus_directional_mov)

	# Calculating -DM1 smoothed values
	nega_directional_mov_smoothed = moving_wilder_smoothing(nega_directional_mov)

	# Calculates +DI and -DI
	pos_directional_index, neg_directional_index, directional_movement_index = find_directional_index(true_range_smoothed, plus_directional_mov_smoothed, nega_directional_mov_smoothed)

	# Calculating average directional index
	avg_direction_index = average_directional_index(directional_movement_index)

	return pos_directional_index, neg_directional_index, avg_direction_index

