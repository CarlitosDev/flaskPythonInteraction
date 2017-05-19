# import the usuals
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import os
import pickle

def read_stocks(listOfSymbols = ['AAPL', 'MSFT'], targetVariable = 'Adj Close', dataSource = 'yahoo'):

    endDT   = dt.datetime.today();
    startDT = endDT - relativedelta(years=1);

    # retrieve data from the web
    mainDF     = pd.DataFrame();
    numSymbols = len(listOfSymbols);

    tickersFolder = 'tickers';

    for count, symbolName in enumerate(listOfSymbols):
        print('({}/{})...'.format(1+count, numSymbols))
        df = getTickerData(symbolName, startDT, endDT, dataSource)
        symbolName  = symbolName.replace(':', '_');
        df.columns  = symbolName;

        # save the ticker
        dataFolder = 'xlsTickers';
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)
        currentFile = os.path.join(dataFolder,'{}'.format(symbolName));
        # to xls 
        xlsFile = currentFile + '.xlsx';
        dataFrameToXLS(df, xlsFile);
        # to pickle
        #pickleFile = currentFile + '.pickle';
        #dataFrameToPickle(df, pickleFile);
        if mainDF.empty:
            mainDF = df
        else:
            mainDF = mainDF.join(df, how='outer') 

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

def dataFrameToPickle(df, currentFile):
    if not df.dropna().empty:
        with open(currentFile,'wb') as f:
            pickle.dump(df,f)

def dataFrameToXLS(df, xlsFile, sheetName = 'DF'):
    if not df.empty:
        xlsWriter = pd.ExcelWriter(xlsFile);
        df.to_excel(xlsWriter, sheetName);
        xlsWriter.save();

def getTickerData(currentTicker, startDT, endDT, dataSource = 'yahoo'):
    df = pd.DataFrame();
    print('Reading {}...'.format(currentTicker))
    try:
        df = web.DataReader(currentTicker, dataSource, startDT, endDT)
    except:
        print('Oops!    Can\'t find that ticker...')
    return df;