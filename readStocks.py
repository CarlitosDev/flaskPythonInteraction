# import the usuals
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_datareader.data as web
import numpy as np

def read_stocks(listOfSymbols = [['AAPL', 'MSFT']], targetVariable = 'Adj Close'):

    endDT   = dt.datetime.today();
    startDT = endDT - relativedelta(years=1);

    # retrieve data from the web
    mainDF         = pd.DataFrame();

    for symbolName in listOfSymbols:
        df = web.DataReader(symbolName, "yahoo", startDT, endDT)[targetVariable]
        df.columns = symbolName;
        mainDF = mainDF.join(df, how='outer');

    return mainDF;

def normaliseStocks(mainDF):

    # save the stats
    dfStats = mainDF.describe();
    minVals = dfStats.ix['min'];
    maxVals = dfStats.ix['max'];
    avgVals = dfStats.ix['mean'];
    symbols = mainDF.columns.values.tolist();

    currentDesc = '';
    for i in range(0,len(symbols)):
        currentDesc += symbols[i] + ' ' + str('%3.2f'%(avgVals[i])) + '\t'

    mainDFNorm = (mainDF - minVals)/(maxVals-minVals);

    return mainDFNorm, minVals, maxVals, avgVals;