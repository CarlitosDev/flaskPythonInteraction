from pandas_highcharts.core import serialize
import pandas as pd
import numpy as np
from pandas.compat import StringIO
from itertools import chain

# import date functionality
import datetime as dt
from dateutil.relativedelta import relativedelta


from numpy import asarray, cumprod, convolve, exp, ones
from numpy.random import lognormal, gamma, uniform

# import Bokeh
from bokeh.charts   import Histogram as bkHistogram
from bokeh.layouts  import row, column, gridplot, row, widgetbox
from bokeh.models   import ColumnDataSource, Slider, Select
from bokeh.plotting import curdoc, figure   
from bokeh.driving  import count
from bokeh.palettes import Spectral5


def getUniformHistogram():
    # create random numbers
    maxValue = 100;
    df = pd.DataFrame(np.random.randint(maxValue, size=(2000, 2)), columns=['randomA', 'randomB'])
    feature_names = df.columns.values.tolist();
    handleHistogram = bkHistogram(df, legend='top_right', width=600, height=400);
    # Set the x axis label
    handleHistogram.xaxis.axis_label = 'Random uniform noise'
    # Set the y axis label
    handleHistogram.yaxis.axis_label = 'Histogram Count'
    return handleHistogram ,feature_names;

def getAutoMPGexample():
    pageTitle = 'example from http://bokeh.pydata.org/en/latest/docs/reference/charts.html#histogram';
    # load the data from Bokeh's sampledata
    from bokeh.sampledata.autompg import autompg as df
    handleHistogram = bkHistogram(df, values='mpg', label='cyl', color='cyl', legend='top_right',
                    title="MPG Histogram by Cylinder Count", plot_width=800);
    return handleHistogram, pageTitle;


def getCrossFilter(df, discrete, x, y, size, color):
    
    SIZES = list(range(6, 22, 3))
    COLORS = Spectral5
    ORIGINS = ['North America', 'Europe', 'Asia']

    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        groups = pd.qcut(df[size.value].values, len(SIZES))
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        groups = pd.qcut(df[color.value].values, len(COLORS))
        c = [COLORS[xx] for xx in groups.codes]
    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p