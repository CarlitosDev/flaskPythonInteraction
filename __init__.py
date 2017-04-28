from flask import Flask, render_template
from readStocks import read_stocks, normaliseStocks
from pandas_highcharts.core import serialize
import pandas as pd
from pandas.compat import StringIO
app = Flask(__name__)

@app.route('/')
def homepage():
	pageTitle   = 'Read my stocks'
	listOfTickers = [['AAPL', 'MSFT', 'TSCO.L', 'SBRY']]
	stocks = read_stocks(listOfSymbols = listOfTickers);
	description = 'Current tickers: ' + str(stocks.columns.values.tolist())[1:-1]
	titleText   = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d')
	stockChart  = serialize(stocks, render_to='stocksChart', output_type='json', title=titleText, chart_type='stock')
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

@app.route('/pie')
def pieChart():
	pageTitle   = 'Pie View'
	description = 'Test pie charts from Python-Highcharts'
	listOfTickers = [['AAPL', 'MSFT', 'TSCO.L', 'SBRY']]
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

if __name__ == "__main__":
    app.run()