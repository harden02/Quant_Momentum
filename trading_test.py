# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:24:13 2022
Tests selection of stocks against their ETF equivalent over specified period and writes results to file
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def trade(raw_log_returns, comparative_log_returns, start_point, comparative_data_file, end_date, interval):
    """
    Parameters
    ----------
    raw_log_returns : Array
        log returns to be used for analysis.
    comparative_log_returns : Array
        log returns in relation to ETF to be used for analysis.
    start_point : INT
        Starting date slice for trading. REMEMBER: STARTING SLICE NEXT INTERVAL AFTER FORMATION, OTHERWISE FORESIGHT BIAS
    comparative_data_file : filepath
        file comparing data for comparison (e.g SPY).
    end_date : DATE
        Ending date of comparative_data_file csv to read, match with end date of your trading data.

    Returns
    -------
    Returns of the strategy.

    """

    raw_strat_returns = raw_log_returns[start_point:end_date] # log returns for hold period
    strategy_return = np.mean(np.exp(raw_strat_returns.sum()))
    plt.style.use('seaborn')
    raw_strat_returns.plot(kind='line', figsize=(24, 15), title='Holding period Return selected equities')
    # plots log returns for visualization of momentum "wave"
    benchmark_strat_returns = comparative_log_returns[start_point:end_date]
    benchmark_return = np.mean(np.exp(benchmark_strat_returns.sum()))
    # same as previous but comparing to ETF as benchmark
    
    print("return in tested holding period:", strategy_return)
    print("performance compared to benchmark in holding period:", benchmark_return)
    
    spy_price_data_raw = pd.read_csv(comparative_data_file, parse_dates=True, index_col="Date")
    spy_price_data = spy_price_data_raw[:end_date] # must be a quicker way of doing this without first reading in csv, look up for future
    spy_price_data_resample = spy_price_data.resample(interval).asfreq()
    spy_final_prices = pd.merge_asof(spy_price_data_resample, spy_price_data, on="Date", allow_exact_matches=True, direction="backward")
    spy_final_prices.dropna(axis=1, inplace=True)
    spy_final_prices.columns = spy_final_prices.columns.str.strip('_y')
    spy_final_prices.set_index("Date", inplace=True)
    # importing SPY for pure benchmark
    spy_log_returns = np.log(spy_final_prices / spy_final_prices.shift(1))  # calculates log returns 
    spy_returns = spy_log_returns[start_point:end_date]  # returns from SPY over hold period
    spy_return = np.exp(spy_returns.sum()) # overall SPY return
    print('performance of SPY in same period was', spy_return)
    return_spy = spy_return.iloc[0] # otherwise junk is written into CSV because of series datatype

    return (strategy_return, benchmark_return, return_spy)