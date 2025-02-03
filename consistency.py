"Best Performers Analysis, creating a stockpool of equitis that have consistently posted higher returns than their relatives"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_outperformers(relative_returns, lookback_date, worst_return):
    """
    Parameters
    ----------
    relative_returns : Array
        Relative performance compared to ETF.
    lookback_date : DATE
        Ending point of performance lookback period
    worst_return : FLOAT
        Minimum acceptable performance for 1 index slice (specified period) for equity to remain in list.

    Returns
    -------
    stock_pool_best_performers : Array
        List of the best performers in the selection.

    """
    
    log_returns_stock_pool = relative_returns.loc[:lookback_date] #CAN DECIDE IF YOU WANT TO KEEP FORMATION PERIOD IN CONSISTENCY BY ADDING IT IN HERE
    plt.style.use('seaborn')
    log_returns_stock_pool.plot(kind='line', figsize=(24, 15), title='Performance relative to ETF in performance period', legend=None)
    min_vals = log_returns_stock_pool.min(axis=0)
    min_vals = pd.DataFrame(min_vals)
    averages = log_returns_stock_pool.mean(axis=0)
    averages = pd.DataFrame(averages)
    best_mins = min_vals[(min_vals[:] >= worst_return)]
    best_mins.dropna(inplace=True)
    best_mins = best_mins.transpose()
    best_averages = averages[(averages[:] >= 0)]
    best_averages.dropna(inplace=True)
    best_averages = best_averages.transpose()
    intersection_cols = log_returns_stock_pool.columns & best_averages.columns & best_mins.columns  #filters for stocks that dont drop below best_min and average outperforming return
    stock_pool_best_performers = log_returns_stock_pool[intersection_cols]
    stock_pool_best_performers.plot(kind='line', figsize=(24, 15), title='Best Performers', legend=None)
    comparative_returns = np.exp(stock_pool_best_performers.sum())
    return stock_pool_best_performers.columns