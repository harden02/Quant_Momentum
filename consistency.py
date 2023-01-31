"Best Performers Analysis, creating a stockpool of equitis that have consistently posted higher returns than their relatives"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_outperformers(relativereturns, lookback_date, worstreturn):
    """
    

    Parameters
    ----------
    relativereturns : Array
        Relative performance compared to ETF.
    lookback_date : DATGE
        Ending point of performance lookback period
    worstreturn : FLOAT
        Minimum acceptable performance for 1 index slice (specified period) for equity to remain in list.

    Returns
    -------
    stockpool_bestperformers : Array
        List of the best performers in the selection.

    """
    
    
    
    logreturns_stockpool=relativereturns.loc[:lookback_date] #CAN DECIDE IF YOU WANT TO KEEP FORMATION PERIOD IN CONSISTENCY BY ADDING IT IN HERE
    plt.style.use('seaborn')
    logreturns_stockpool.plot(kind='line', figsize=(24, 15), title='Performance relative to ETF in performance period', legend=None)
    minvals=logreturns_stockpool.min(axis=0)
    minvals=pd.DataFrame(minvals)
    averages=logreturns_stockpool.mean(axis=0)
    averages=pd.DataFrame(averages)
    bestmins = minvals[(minvals[:]>=(worstreturn))]
    bestmins.dropna(inplace=True)
    bestmins=bestmins.transpose()
    bestaverages = averages[(averages[:]>=0)]
    bestaverages.dropna(inplace=True)
    bestaverages=bestaverages.transpose()
    intersection_cols = logreturns_stockpool.columns & bestaverages.columns & bestmins.columns  #filters for stocks that dont drop below bestmin and average outperforming return
    stockpool_bestperformers = logreturns_stockpool[intersection_cols]
    stockpool_bestperformers.plot(kind='line', figsize=(24, 15), title='Best Performers', legend=None)
    comparativereturns=np.exp(stockpool_bestperformers.sum())
    return stockpool_bestperformers.columns