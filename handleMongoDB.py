# import the usuals
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from pymongo import MongoClient
from readStocks import read_stocks, normaliseStocks
import pprint
import json

client = MongoClient('mongodb://localhost:27017/')

# create a collection named 'yahooStocks'
db = client['yahooStocks']
stocksCollection = db['stocksCollection']

# read the collection of stocks
listOfTickers = [['AAPL', 'MSFT']]
stocks = read_stocks(listOfSymbols = listOfTickers);

# 
stocks.index = stocks.index.astype(str)

stocksAsDict = stocks.to_dict('index');
result = stocksCollection.insert_many(stocksAsDict)
records = json.loads(stocks.to_json()).values()
result = stocksCollection.insert_many(records)
# insert into mongoDB - use the option 'records' to keep the columnnames
result = stocksCollection.insert_many(stocks.to_dict('records'));
#result = stocksCollection.insert_many(stocks.to_dict('index'));
# check the process went well
result.inserted_ids

pprint.pprint(stocksCollection.find_one())

# retrieve as a DF
df = pd.DataFrame(list(stocksCollection.find()))
df.describe()
# stocksCollection.remove() to drop them all