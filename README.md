# flask Python Interaction
Proof of concept for a Google Cloud project. The current repository holds Python code to retrieve a list of tickers from Yahoo finance and plot them in a website using Flask and pandas_highcharts, a interface from Pandas to the Highcharts visualisation library.

Comments:
-------
* 17/05/2017 Yahoo has changed the API so pandas_datareader is currently retrieving empty dataframes.
* 24/05/2017 Trying Bokeh!


Requirements:
-------
* pip install flask
* pip install pandas_highcharts
* pip install pymongo
* pip install Flask-PyMongo
* pip install bokeh
* easy_install quandl

Test it:
-------
1. Make sure MongoDB is running (mongod)
1. python __init__.py
1. http://127.0.0.1:5000/


## Current views
1. http://127.0.0.1:5000/scatterPlot
1. http://127.0.0.1:5000/streamPlot
1. http://127.0.0.1:5000/ticker/<tickername>
1. http://127.0.0.1:5000/bokehTest
1. http://127.0.0.1:5000/bokehTest2  (down)
1. http://127.0.0.1:5000/bokehTest3
1. http://127.0.0.1:5000/cubeView (down)
1. http://127.0.0.1:5000/polar (down)
1. http://127.0.0.1:5000/pie (down)


```python
__init__.py
```



