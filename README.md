A very basic initial attempt at using code to determine possibly buy signals in a simple momentum based strategy. Used to experiment with the yfinance package and apply some learnings of using Python for finance.

consistency.py:
A function which analyzes the equities within the chosen pool/ETF to determine which have consistently shown better performance than others. (Obviously it is no true indication of future performance as I have since learned)

csvtoprices.py:
Two functions which read in a csv which I had created by downloading data from yfinance, and then creating a dataframe of logarithmic returns with them.

momentumanalysis.py:
A function to pick out the equity symbols within the group which displayed the greatest upward trend, either by start vs finish price or by a polynomical/exponential increase

tradingtest.py:
"Buy" a set of equities as an input dataframe and calculate the returns over a given holding period, with comparisons to other S&P500 benchmarks

modulartest.py:
end to end test of the above

These went on to form the basis of the quantlibrary repo: https://github.com/harden02/QuantLibrary
