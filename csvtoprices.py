"""Modularised data processor for S&P500 csv data (will extend to any stockprice csv eventuaolly)"""
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

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
    pricedataresample = pricedata.resample(interval).asfreq()
    finalprices = pd.merge_asof(pricedataresample, pricedata, on = "Date", allow_exact_matches = True, direction = "backward")
    finalprices.dropna(axis=1, inplace=True)
    finalprices.columns = finalprices.columns.str.strip('_y')
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
        


