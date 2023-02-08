# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:24:13 2022
Tests selection of stocks against their ETF equivalent over specified period and writes results to file
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def trade(rawlogreturns, comparativelogreturns, startpoint, comparativedatafile, enddate):
    """
    

    Parameters
    ----------
    rawlogreturns : Array
        log returns to be used for analysis.
    comparativelogreturns : Array
        log returns in relation to ETF to be used for analysis.
    startpoint : INT
        Starting date slice for trading. REMEMBER: STARTING SLICE NEXT INTERVAL AFTER FORMATION, OTHERWISE FORESIGHT BIAS
    comparativedatafile : filepath
        file comparing data for comparison (e.g SPY).
    enddate : DATE
        Ending date of comparativedatafile csv to read, match with end date of your trading data.

    Returns
    -------
    Returns of the strategy.

    """

    rawstratreturns=rawlogreturns[startpoint:enddate] #log returns for hold period
    strategyreturn=np.mean(np.exp(rawstratreturns.sum()))
    plt.style.use('seaborn')
    rawstratreturns.plot(kind='line', figsize=(24, 15), title='Holding period Return selected equities')
    #plots log returns for visualization of momentum "wave"
    benchmarkstratreturns=comparativelogreturns[startpoint:enddate]
    benchmarkreturn=np.mean(np.exp(benchmarkstratreturns.sum()))
    #same as previous but comparing to ETF as benchmark
    
    print("return in tested holding period:", strategyreturn)
    print("performance compared to benchmark in holding period:", benchmarkreturn)
    
    SPYpricedata = pd.read_csv(comparativedatafile, parse_dates = True, index_col = "Date")
    SPYpricedata = SPYpricedata[startpoint:enddate] 
    SPYpricedata = SPYpricedata.resample("B").asfreq().ffill()
    SPYpricedata = SPYpricedata.resample("3BMS").asfreq()
    SPYpricedata.dropna(inplace=True)
    #importing SPY for pure benchmark
    SPYlogreturns=np.log(SPYpricedata/SPYpricedata.shift(1))  #calculates log returns 
    SPYreturns = SPYlogreturns[startpoint:enddate]  #returns from SPY over hold period
    SPYreturn = np.exp(SPYreturns.sum()) #overall SPY return
    print('performance of SPY in same period was', SPYreturn)
    returnSPY = SPYreturn.iloc[0] #otherwise junk is written into CSV because of series datatype

    return (strategyreturn, benchmarkreturn, returnSPY)