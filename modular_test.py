# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 17:53:13 2022

End to end test of modularised code to ensure correct operation
"""
import math
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
import csv_to_prices
import consistency
import momentum_analysis
import trading_test

"""Set Variables from here"""

file = 'S&P500pricesadj.csv'
start_date = '2012-12-31'
end_date = '2018-12-31'
etf_name = "IVV"
interval = 'Q'
lookback_date = '2017-12-31'
worst_return = -0.15
formation_start = '2017-09-30'
formation_end = '2018-03-31'
r_squared = 0.6
slope = 0
use_gradient = False
trade_start_point = '2018-06-30'
comparative_data_file = 'SPYpricesadj.csv'
trade_end_date = '2018-12-31'
return_file = "MomentumReturnsModular.txt"

price_data = csv_to_prices.read_stock_csv(file, start_date, end_date, etf_name, interval)
log_returns = csv_to_prices.log_return(price_data, etf_name)

best_performers = consistency.get_outperformers(relative_returns=log_returns['relative_log_returns'], 
                                                lookback_date=lookback_date, 
                                                worst_return=worst_return)

momentum = momentum_analysis.momentum_analyse(equity_log_returns=(log_returns['log_returns'])[best_performers], 
                                              formation_start=formation_start, 
                                              formation_end=formation_end, 
                                              r_squared=r_squared, 
                                              slope=slope,
                                              use_gradient=use_gradient)

results = trading_test.trade(raw_log_returns=(log_returns['log_returns'])[best_performers].loc[:, momentum], 
                             comparative_log_returns=(log_returns['relative_log_returns'])[best_performers].loc[:, momentum], 
                             start_point=trade_start_point, 
                             comparative_data_file=comparative_data_file, 
                             end_date=trade_end_date,
                             interval=interval)

#with open(return_file, "a") as results_file:
    #results_file.write(f"\n{start_date},{end_date},{trade_start_point},{worst_return},{r_squared}, {use_gradient}, {results[0]},{results[1]},{results[2]}")
# writes results to txt file in csv format

test = log_returns['log_returns']['IVV']
test = test[trade_start_point:trade_end_date]
test = np.exp(test.sum())

"""SPY_price_data = pd.read_csv(comparative_data_file, parse_dates=True, index_col="Date")
SPY_price_data = SPY_price_data[start_date:trade_end_date] 
SPY_price_data = SPY_price_data.resample("B").asfreq().ffill()
SPY_price_data = SPY_price_data.resample("3BMS").asfreq()
SPY_price_data.dropna(inplace=True)
#importing SPY for pure benchmark
SPY_log_returns = np.log(SPY_price_data / SPY_price_data.shift(1))  # calculates log returns 
SPY_returns = SPY_log_returns[trade_start_point:trade_end_date]  # returns from SPY over hold period
SPY_return = np.exp(SPY_returns.sum()) # overall SPY return"""

"""price_data_raw = pd.read_csv(file, parse_dates=True, infer_datetime_format=True, index_col="Date")
price_data = price_data_raw[start_date:end_date] # must be a quicker way of doing this without first reading in csv, look up for future
price_data_resample = price_data.resample(interval).asfreq()
final_prices = pd.merge_asof(price_data_resample, price_data, on="Date", allow_exact_matches=True, direction="backward")
final_prices.dropna(axis=1, inplace=True)
final_prices.columns = final_prices.columns.str.strip('_y')
final_prices.set_index("Date", inplace=True)
# it works wooooo"""

# def run(file, start_date, end_date, etf_name, interval, formation_start, formation_end, r_squared, slope, use_gradient)
