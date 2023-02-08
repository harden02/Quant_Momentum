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
startdate = '2010-12-01'
enddate = '2016-12-05'
ETFname = "IVV"
interval = '3BMS'
lookback_date = '2015-12-01'
worstreturn = -0.15
formation_start = '2015-06-01'
formation_end = '2015-12-01'
Rsquared = 0.6
slope = 0
use_gradient = False
tradestartpoint = '2016-03-01'
comparativedatafile = 'SPYpricesadj.csv'
tradeenddate = '2016-09-01'
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
                            enddate = tradeenddate)

with open(returnfile, "a") as results_file:
    results_file.write(f"\n{startdate},{enddate},{tradestartpoint},{worstreturn},{Rsquared}, {use_gradient}, {results[0]},{results[1]},{results[2]}")
#writes results to txt file in csv format

#it works wooooo

#def run(file, startdate, enddate, ETFname, interval, formation_start, formation_end, Rsquared, slope, use_gradient )
