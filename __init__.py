from flask import Flask, render_template
from readStocks import read_stocks, normaliseStocks
from pandas_highcharts.core import serialize
app = Flask(__name__)

@app.route('/')
def homepage():
	pageTitle   = 'Read my stocks'
	stocks      = read_stocks()
	description = 'Current tickers: ' + str(stocks.columns.values.tolist())[1:-1]
	titleText   = 'from ' + stocks.index[0].strftime('%Y-%m-%d') + ' to ' + stocks.index[-1].strftime('%Y-%m-%d')
	titleLabel  = {"text": titleText}
	stockChart  = serialize(stocks, render_to='stocksChart', output_type='json', title=titleText)
	return render_template("index.html", pageTitle=pageTitle, paragraph=description, chart=stockChart)

if __name__ == "__main__":
    app.run()