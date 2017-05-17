# import the usuals
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import os

def read_stocks(listOfSymbols = [['AAPL', 'MSFT']], targetVariable = 'Adj Close'):

    endDT   = dt.datetime.today();
    startDT = endDT - relativedelta(years=1);

    # retrieve data from the web
    mainDF     = pd.DataFrame();
    numSymbols = len(listOfSymbols[0]);

    for count, symbolName in enumerate(listOfSymbols[0]):
        print('Reading {}{}/{}...'.format(symbolName, 1+count, numSymbols))
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


def getTickersList(xlsFile=[]):
    if not bool(xlsFile):
        fName     = 'listOfTickers.xlsx';
        xlsRoot   = '/Users/carlosAguilar/Documents/PythonDev/Coding/flaskPythonInteraction';
        xlsFile   = os.path.join(xlsRoot, fName)
    df = pd.read_excel(xlsFile)
    return df;