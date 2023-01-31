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

pricedata = csvtoprices.readstockcsv('S&P500pricesadj.csv',
                         '2010-12-01', '2016-12-05', "IVV", '3BMS')
logreturns = csvtoprices.logreturn(pricedata, "IVV")

best_performers = consistency.get_outperformers(relativereturns = logreturns['relativelogreturns'], 
                                                lookback_date = '2015-12-01', 
                                                worstreturn = -0.15)

momentum = momentumanalysis.momentumanalyse(equitylogreturns = (logreturns['logreturns'])[best_performers], 
                                            formation_start = '2015-06-01', 
                                            formation_end = '2015-12-01', 
                                            Rsquared = 0.6, 
                                            slope = 0,
                                            use_gradient = False)

results = tradingtest.trade(rawlogreturns=(logreturns['logreturns'])[best_performers].loc[:,momentum], 
                            comparativelogreturns = (logreturns['relativelogreturns'])[best_performers].loc[:,momentum], 
                            startpoint = '2016-03-01', 
                            comparativedatafile = 'SPYpricesadj.csv', 
                            startdate = '2016-03-01', 
                            enddate = '2016-12-01', 
                            returnfile = "MomentumReturnsModular.txt", 
                            worstreturn = -0.15, Rsquared = 0.6)

#it works wooooo

#def run(file, startdate, enddate, ETFname, interval, formation_start, formation_end, Rsquared, slope, use_gradient )
