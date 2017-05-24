from flask import Flask, render_template
from flask_pymongo import PyMongo
from readStocks import read_stocks, normaliseStocks, getTickersList
from pandas_highcharts.core import serialize
import pandas as pd
import numpy as np
from pandas.compat import StringIO
from itertools import chain
from mpl_toolkits.mplot3d import axes3d
app = Flask(__name__)

@app.route('/')
def homepage():
    # data
	tickersData   = getTickersList();
	# Form the COUNTRY:
	# tickersGoogle = tickersData['Exchange'] + ':' +   tickersData['Ticker'];
	tickersGoogle  = tickersData['Ticker'];
	listOfTickers  = tickersGoogle.tolist();
	dataSource     = 'google';
	targetVariable = 'Close';
	stocks = read_stocks(listOfSymbols = listOfTickers, targetVariable = targetVariable, datasource = dataSource);
	#stocks = read_stocks(listOfSymbols = listOfTickers);
    # web content
	pageTitle   = 'Read my stocks'
	description = 'Current tickers: ' + str(stocks.columns.values.tolist())[1:-1]
	titleText   = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d')
	stockChart  = serialize(stocks, render_to='stocksChart', output_type='json', title=titleText, chart_type='stock')
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

@app.route('/pie')
def pieChart():
	pageTitle   = 'Pie View'
	description = 'Test pie charts from Python-Highcharts'
	listOfTickers = [['AAPL', 'MSFT', 'TSCO.L', 'SBRY']];
	stocks = read_stocks(listOfSymbols = listOfTickers);
	df = pd.DataFrame(stocks.mean(), columns=['avgPrice']);
	df['total'] = 1
	stockChart = serialize(df, render_to="stocksChart", kind="pie",  y=['avgPrice'], title='AveragePrice', 
		tooltip={'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'}, output_type='json')
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

@app.route('/polar')
def polarChart():
	pageTitle   = 'Polar View'
	description = 'This should be a polar chart according to the documentation';
	listOfTickers = [['AAPL', 'MSFT', 'TSCO.L', 'SBRY']];
	stocks = read_stocks(listOfSymbols = listOfTickers);
	df = pd.DataFrame(stocks.mean(), columns=['avgPrice']);
	df.fillna(0, inplace=True);
	stockChart = serialize(df, render_to="stocksChart", polar=True, kind='bar', title='AveragePrice',  output_type='json')
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

@app.route('/cubeView')
def cubeView():
	pageTitle     = 'Cube visualisation of my stocks';
	listOfTickers = [['AAPL', 'MSFT', 'TSCO.L', 'SBRY', 'BP', 'REP.MC']];
	stocks        = read_stocks(listOfSymbols = listOfTickers);
	df            = pd.DataFrame([stocks.mean(), stocks.max()]);
	df.fillna(0, inplace=True);
	label1        = 'average value';
	label2        = 'max value';
	avgValues     = df.ix[0].values.tolist();
	maxValues     = df.ix[1].values.tolist();
	categories    = list(chain.from_iterable(listOfTickers));
	description   = 'Current tickers: ' + str(stocks.columns.values.tolist())[1:-1];
	titleText     = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d');
	return render_template("cubeView.html", pageTitle=pageTitle, paragraph=description, categories=categories, 
		titleText=titleText, label1=label1, label2=label2, avgValues=avgValues, maxValues=maxValues);

@app.route('/scatterPlot')
def scatterPlot():
	pageTitle   = '3D scatter plot'
	description = 'Test 3D charts from (pure) Highcharts'
	# create random numbers
	maxValue = 100;
	df = pd.DataFrame(np.random.randint(maxValue, size=(20, 3)), columns=list('XYZ'))
	xMax, yMax, zMax = df.max();
	# df as a list
	dataToPlot = df.values.tolist();
	return render_template("scatter3DView.html", pageTitle=pageTitle, paragraph=description, 
		plotValues=dataToPlot, xMax = xMax, yMax=yMax, zMax=zMax)

@app.route('/streamPlot')
def streamPlot():
	pageTitle   = '3D stream plot'
	description = 'Import some test data from mpl_toolkits.mplot3d'
	# Get the test data
	X, Y, Z    = axes3d.get_test_data(0.5)
	numR, numC = X.shape
	# Append the data
	dTemp = pd.DataFrame();
	df    = pd.DataFrame();
	for i in range(0,numR-1):
		if df.empty:
			df['X'] = X[i]
			df['Y'] = Y[i]
			df['Z'] = Z[i]
		else:
			dTemp['X'] = X[i]
			dTemp['Y'] = Y[i]
			dTemp['Z'] = Z[i]
			# ought to return 'df' as there's no 'inplace' for append
			df = df.append(dTemp, ignore_index=True);
	# make sure the values are >0
	df['Z'] = 100*df['Z'];
	df = abs(df);
	xMax, yMax, zMax = df.max();
	# df as a list
	dataToPlot = df.values.tolist();
	return render_template("scatter3DView.html", pageTitle=pageTitle, paragraph=description, 
		plotValues=dataToPlot, xMax = xMax, yMax=yMax, zMax=zMax)


if __name__ == "__main__":
    app.run()