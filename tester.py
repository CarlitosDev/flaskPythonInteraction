from readStocks import normaliseStocks, getTickersList, getTickerData, dataFrameToXLS
from pandas_highcharts.core import serialize
import pandas as pd
from pandas.compat import StringIO
from itertools import chain
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas_datareader.data as web
import os

# data
tickersData    = getTickersList();
# Form the COUNTRY:
tickersGoogle  = tickersData['Ticker'];
listOfTickers  = tickersGoogle.tolist();
dataSource     = 'google';
targetVariable = 'Adj Close';

for count, symbolName in enumerate(listOfTickers):
    df = getTickerData(symbolName, startDT, endDT, dataSource = dataSource)
    # save the ticker
    dataFolder = 'xlsTickers';
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder);
    currentFile = os.path.join(dataFolder,'{}'.format(symbolName));
    # to xls
    if not df.empty:
        xlsFile = currentFile + '.xlsx';
        dataFrameToXLS(df, xlsFile);