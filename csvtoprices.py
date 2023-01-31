"""Modularised data processor for S&P500 csv data (will extend to any stockprice csv eventuaolly)"""
import numpy as np
import pandas as pd

#Takes in local S&P500 csv in this folder and processes it for stock close prices over a certain time period and interval
#Generates logarithmic returns file and log returns in relation to the ETF that is being tracked


def readstockcsv(file, startdate, enddate, ETFname, interval):
    """
    

    Parameters
    ----------
    file : path
        csv of stock prices to be read.
    startdate : DATE
        start date for analysis.
    enddate : DATE
        end date for analysis.
    ETFname : STRING
        ticker symbol for ETF present in the stock file that it's following.
    interval : STRING
        interval to sample, i.e 3BMS for 3 business months or B for each business day.

    Returns
    -------
    finalprices : ARRAY
        Resampled and corrected stock prices.

    """
    
    pricedataraw = pd.read_csv(file, parse_dates = True, infer_datetime_format=(True), index_col = "Date")
    pricedata = pricedataraw[startdate:enddate] #must be a quicker way of doing this without first reading in csv, look up for future
    pricedata = pricedata.resample(interval).asfreq()
    pricedatashifted = pricedata.copy()
    pricedatashifted.index=np.where(pricedatashifted.isna().all(axis=1), pricedatashifted.index.shift(1, freq='B'), pricedatashifted.index)
    finalprices=pricedataraw.loc[pricedatashifted.index]
    finalprices.index.names = ['Date']
    finalprices.dropna(axis=1, inplace=True)
    
    #pricedata = pd.read_csv(file, parse_dates = True, index_col = "Date")
    #pricedata = pricedata[startdate:enddate] #must be a quicker way of doing this without first reading in csv, look up for future
    #pricedata = pricedata.resample("B").asfreq().ffill() #required to fill in the missing days that pandas will force resample instead of just realising to go 1 forward
    #pricedata = pricedata.resample(interval).asfreq()
    #pricedata.dropna(subset=[ETFname], inplace=True)
    #pricedata.dropna(axis=1, inplace=True)
    #if len(pricedata) < 25:
        #raise Exception("Pricedata not long enough, adjust dates so they don't fall on holidays!")
    return finalprices


def logreturn(stockdata, ETFname):
    """
    

    Parameters
    ----------
    stockdata : ARRAY
        stock price array to calculate log returns on.
    ETFname : SRRING
        ETF name.

    Returns
    -------
    dict
        returns a dictionary containing two arrays, absolute log returns and log returns relative to ETF.

    """
    logreturns=np.log(stockdata/stockdata.shift(1))  #calculates log returns for each
    relativelogreturns=pd.DataFrame()  #have to create new dataframe otherwise following part doesn't work
    for column in logreturns:  
        relativelogreturns[column]=logreturns[column]-logreturns[ETFname]  #compares log returns to those of ETF
    return {"logreturns" : logreturns, "relativelogreturns" :relativelogreturns}
        


