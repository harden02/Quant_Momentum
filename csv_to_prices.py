"""Modularised data processor for S&P500 csv data (will extend to any stockprice csv eventuaolly)"""
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

#Takes in local S&P500 csv in this folder and processes it for stock close prices over a certain time period and interval
#Generates logarithmic returns file and log returns in relation to the ETF that is being tracked


def read_stock_csv(file, start_date, end_date, etf_name, interval):
    """
    Parameters
    ----------
    file : STRING
        path to the stock file.
    start_date : DATE
        start date for analysis.
    end_date : DATE
        end date for analysis.
    etf_name : STRING
        ticker symbol for ETF present in the stock file that it's following.
    interval : STRING
        interval to sample, i.e 3BMS for 3 business months or B for each business day.

    Returns
    -------
    final_prices : ARRAY
        Resampled and corrected stock prices.

    """
    
    price_data_raw = pd.read_csv(file, parse_dates=True, infer_datetime_format=True, index_col="Date")
    price_data = price_data_raw[start_date:end_date] #must be a quicker way of doing this without first reading in csv, look up for future
    price_data_resample = price_data.resample(interval).asfreq()  
    final_prices = pd.merge_asof(price_data_resample, price_data, on="Date", allow_exact_matches=True, direction="backward")
    final_prices.dropna(axis=1, inplace=True)
    final_prices.columns = final_prices.columns.str.strip('_y')
    final_prices.set_index("Date", inplace=True)
    return final_prices


def log_return(stock_data, etf_name):
    """
    Parameters
    ----------
    stock_data : ARRAY
        stock price array to calculate log returns on.
    etf_name : STRING
        ETF name.

    Returns
    -------
    dict
        returns a dictionary containing two arrays, absolute log returns and log returns relative to ETF.

    """
    log_returns = np.log(stock_data / stock_data.shift(1))  # calculates log returns for each
    relative_log_returns = pd.DataFrame()  # have to create new dataframe otherwise following part doesn't work
    for column in log_returns:  
        relative_log_returns[column] = log_returns[column] - log_returns[etf_name]  # compares log returns to those of ETF
    return {"log_returns": log_returns, "relative_log_returns": relative_log_returns}
        
