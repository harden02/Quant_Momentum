# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:53:35 2022
Modularised analysis of logarithmic return to identify exponential returns on momentum performing equities
Consider expanding to look for equities without inflection points
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import math




def momentumanalyse(equitylogreturns, formation_start, formation_end, Rsquared, slope, use_gradient):
    """
    

    Parameters
    ----------
    equitylogreturns : Array
        Collection of equities to be analysed.
    formation_start : DATE
        Date slice of array to start initial formation period analysis.
    formation_end : DATE
        Date slice of array to provide endpoint of formation period analysis.
    Rsquared : FLOAT
        Correlation coefficient for momentum analysis.
    slope : FLOAT
        Gradient of logarithmic returns analysis required to be selected as potential pick.
    use_gradient : Boolean
        Determines if momentum should be measured by a steady increase in log returns (gradient) or by the highest returns over the period

    Returns
    -------
    List of indexes of original array representing equities that meet momentum requirements set.
    """
        

    momentumreturns=equitylogreturns.loc[formation_start:formation_end] #looks at raw log returns in year before holding period
    
    if use_gradient == True:
        
        straightreturns = np.exp(momentumreturns.sum())
        toppercent = math.floor(0.2*len(straightreturns))
        highestmomentum = straightreturns.nlargest(n=toppercent, keep='first')
        return highestmomentum.index
        
    else:
        
        momentumreturns.drop(columns=momentumreturns.columns[momentumreturns.mean()<0], inplace=True)
        momentumreturns.drop(columns=momentumreturns.columns[momentumreturns.iloc[-1]<0], inplace=True)
        plt.style.use('seaborn')
        momentumreturns.plot(kind='line', figsize=(24, 15), title='log returns formation period', legend=None)
        regressreturns=momentumreturns.to_numpy()
        regressreturns=regressreturns.transpose()
        X=np.arange(len(regressreturns[0]))
        corrcoeff=np.empty((0, 2), float)
        for row in regressreturns:  #runs least squares regression on each row to work out movement of returns
            result=stats.linregress(x=X, y=row)
            corrcoeff=np.append(corrcoeff, [[result.slope, result.rvalue]], axis=0)
        #creates array with gradients in 1st column and corr coefficients in 2nd
        
        goodindexes=[]
        for i in range(len(corrcoeff)):
            print(i)
            if (corrcoeff[i, 1])**2 > (Rsquared) and corrcoeff[i, 0] > 0:  #CONDITION FOR STOCK PICKING
                goodindexes.append(i)
        momentumreturns = momentumreturns.iloc[:,goodindexes]
        return momentumreturns.columns #creates list of indexes with a correlation coefficient greater than Rsquared choice to pick
