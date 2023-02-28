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
import csvtoprices
import consistency
import momentumanalysis
import tradingtest

"""Set Variables from here"""

file = 'S&P500pricesadj.csv'
startdate = '2011-12-31'
enddate = '2017-12-31'
ETFname = "IVV"
interval = 'Q'
lookback_date = '2016-12-31'
worstreturn = -0.15
formation_start = '2016-09-30'
formation_end = '2017-03-31'
Rsquared = 0.6
slope = 0
use_gradient = False
tradestartpoint = '2017-06-30'
comparativedatafile = 'SPYpricesadj.csv'
tradeenddate = '2017-12-31'
returnfile = "MomentumReturnsModular.txt"

pricedata = csvtoprices.readstockcsv(file, startdate, enddate, ETFname, interval)
logreturns = csvtoprices.logreturn(pricedata, ETFname)

best_performers = consistency.get_outperformers(relativereturns = logreturns['relativelogreturns'], 
                                                lookback_date = lookback_date, 
                                                worstreturn = worstreturn)

momentum = momentumanalysis.momentumanalyse(equitylogreturns = (logreturns['logreturns'])[best_performers], 
                                            formation_start = formation_start, 
                                            formation_end = formation_end, 
                                            Rsquared = Rsquared, 
                                            slope = slope,
                                            use_gradient = use_gradient)

results = tradingtest.trade(rawlogreturns=(logreturns['logreturns'])[best_performers].loc[:,momentum], 
                            comparativelogreturns = (logreturns['relativelogreturns'])[best_performers].loc[:,momentum], 
                            startpoint = tradestartpoint , 
                            comparativedatafile = comparativedatafile, 
                            enddate = tradeenddate,
                            interval = interval)

with open(returnfile, "a") as results_file:
    results_file.write(f"\n{startdate},{enddate},{tradestartpoint},{worstreturn},{Rsquared}, {use_gradient}, {results[0]},{results[1]},{results[2]}")
#writes results to txt file in csv format

test = logreturns['logreturns']['IVV']
test = test[tradestartpoint:tradeenddate]
test = np.exp(test.sum())


"""SPYpricedata = pd.read_csv(comparativedatafile, parse_dates = True, index_col = "Date")
SPYpricedata = SPYpricedata[startdate:tradeenddate] 
SPYpricedata = SPYpricedata.resample("B").asfreq().ffill()
SPYpricedata = SPYpricedata.resample("3BMS").asfreq()
SPYpricedata.dropna(inplace=True)
#importing SPY for pure benchmark
SPYlogreturns=np.log(SPYpricedata/SPYpricedata.shift(1))  #calculates log returns 
SPYreturns = SPYlogreturns[tradestartpoint:tradeenddate]  #returns from SPY over hold period
SPYreturn = np.exp(SPYreturns.sum()) #overall SPY return"""

"""pricedataraw = pd.read_csv(file, parse_dates = True, infer_datetime_format=(True), index_col = "Date")
pricedata = pricedataraw[startdate:enddate] #must be a quicker way of doing this without first reading in csv, look up for future
pricedataresample = pricedata.resample(interval).asfreq()
finalprices = pd.merge_asof(pricedataresample, pricedata, on = "Date", allow_exact_matches = True, direction = "backward")
finalprices.dropna(axis=1, inplace=True)
finalprices.columns = finalprices.columns.str.strip('_y')
finalprices.set_index("Date", inplace=True)
#it works wooooo"""

#def run(file, startdate, enddate, ETFname, interval, formation_start, formation_end, Rsquared, slope, use_gradient )
