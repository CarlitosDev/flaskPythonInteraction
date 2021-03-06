from flask import Flask, render_template
from flask_pymongo import PyMongo
from readStocks import read_stocks, normaliseStocks, getTickersList, getTickerData
from pandas_highcharts.core import serialize
import pandas as pd
import numpy as np
from pandas.compat import StringIO
from itertools import chain
# import matplotlib toolkits to get some data
from mpl_toolkits.mplot3d import axes3d
# import Bokeh
from bokeh.embed import components
# import date functionality
import datetime as dt
from dateutil.relativedelta import relativedelta
from bokehFunctions import *
from testData import getCrossFilterData
from bokeh.embed import autoload_server
import subprocess
import atexit

app = Flask(__name__)

bokeh_process = subprocess.Popen(
    ['bokeh', 'serve','--allow-websocket-origin=localhost:5000','bokehSliders.py'], stdout=subprocess.PIPE)

@atexit.register
def kill_server():
    print('Bokeh server killed')
    bokeh_process.kill()

# declare here any dataset so it will be global
#...
#...


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


# try on-the-fly visualisation
@app.route('/ticker/<tickername>')
def tickerOnTheFly(tickername):
	dataSource  = 'google';
	print('Selecting {}'.format(tickername))
	endDT       = dt.datetime.today();
	startDT     = endDT - relativedelta(years=1);
	df          = getTickerData(tickername, startDT, endDT, dataSource);
	stocks      = df[['Open', 'Close']];
    # web content
	pageTitle   = 'Ticket on the fly'
	description = 'Tickers: ' + tickername;
	titleText   = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d')
	stockChart  = serialize(stocks, render_to='stocksChart', output_type='json', title=titleText, chart_type='stock')
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

# BOKEH functionality

@app.route('/bokehTest')
def bokehView():
	pageTitle = 'testerFields';
	handleHistogram, feature_names = getUniformHistogram();
	# Embed plot into HTML via Flask Render
	script, div = components(handleHistogram)
	return render_template("bokehRender.html", script=script, div=div, pageTitle=pageTitle)

@app.route('/bokehTest2')
def bokehView2():
	# get autoMPG example
	hist2, pageTitle = getAutoMPGexample();
	# Embed plot into HTML via Flask Render
	script, div = components(hist2)
	
	# Add more stuff
	#slider1 = Slider(start=0, end = 100, value = 50, step = 1, title = "Mag")
	#slider2 = Slider(start=0, end = 100, value = 50, step = 1, title = "test")
	#plots = {'Red': hist2, 'Blue': hist2}
	#script, div = components(plots)
	#script, div = components({"hist2": hist2, "slider1":vform(slider1), "slider2":vform(slider2)})
	# Embed plot into HTML via Flask Render
	return render_template("bokehRender.html", script=script, div=div, pageTitle=pageTitle)

@app.route('/bokehTest3')
def bokehView3():
	pageTitle = 'la paginita de prueba'
	df, columns, discrete, continuous, quantileable = getCrossFilterData();
	x = Select(title='X-Axis', value='mpg', options=columns)
	y = Select(title='Y-Axis', value='hp', options=columns)
	size = Select(title='Size', value='None', options=['None'] + quantileable)
	color = Select(title='Color', value='None', options=['None'] + quantileable)

	# get the crossfilter example
	figHandle = getCrossFilter(df, discrete, x, y, size, color);
	
	#layout = row(controls, figHandle)
	#controls  = widgetbox([x, y, color, size], width=200)
	#x.on_change('value', update)
	#y.on_change('value', update)
	#size.on_change('value', update)
	#color.on_change('value', update)
	#curdoc().add_root(layout)
	#curdoc().title = "Crossfilter"

	# Embed plot into HTML via Flask Render
	script, div = components(figHandle)
	return render_template("bokehRender.html", script=script, div=div, pageTitle=pageTitle)


# use the deployment Bokeh server
#  bokeh serve --host localhost:5000 --host localhost:5006 bokehSliders.py
@app.route('/bokehSliders')
def bokehView4():
	script = autoload_server(model=None, app_path="/bokehSliders")
	return render_template('bokehSliders.html', bokeh_script=script)


def stupidTester():
	tickername  = 'AAPL'
	dataSource  = 'google'; 	
	endDT       = dt.datetime.today();
	startDT     = endDT - relativedelta(years=1);
	df          = getTickerData(tickername, startDT, endDT, dataSource);
	df['MvAvg'] = pd.rolling_mean(df['Close'], window=3, min_periods=1)
	stocks      = df[['Open', 'Close', 'MvAvg']];
	# web content
	pageTitle   = 'Ticket on the fly'
	description = 'Tickers: ' + tickername;
	titleText   = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d')
	stockChart  = serialize(stocks, render_to='stocksChart', output_type='json', title=titleText, chart_type='stock')


# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)



pageTitle   = 'Pie View'
description = 'Test pie charts from Python-Highcharts'
listOfTickers = [['BTCUSD', 'BTCEUR', 'BTCGBP']];
stocks = read_stocks(listOfSymbols = listOfTickers);
df = pd.DataFrame(stocks.mean(), columns=['avgPrice']);
listOfTickers  = tickersGoogle.tolist();
dataSource     = 'google';
stocks = read_stocks(listOfSymbols = listOfTickers, datasource = dataSource);
dataSource  = 'google'; 	
endDT       = dt.datetime.today();
startDT     = endDT - relativedelta(years=1);
tickername  = 'BTCUSD'
df          = getTickerData(tickername, startDT, endDT, dataSource);

tickername  = 'BTC'
df          = getTickerData(tickername, startDT, endDT, dataSource);

import pandas_datareader.data as web
jpy = web.DataReader('DEXJPUS', 'fred')
jpy = web.DataReader('DEXJPUS', 'fred')

# Read BITCOIN exchange rate
import quandl
df = pd.DataFrame(quandl.get("BCHARTS/COINBASEGBP",  start_date="2016-02-11", end_date="2017-12-31"))