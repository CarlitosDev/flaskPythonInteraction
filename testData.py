import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg

def getCrossFilterData():
    df = autompg.copy()

    SIZES = list(range(6, 22, 3))
    ORIGINS = ['North America', 'Europe', 'Asia']

    # data cleanup
    df.cyl = [str(x) for x in df.cyl]
    df.origin = [ORIGINS[x-1] for x in df.origin]

    df['year'] = [str(x) for x in df.yr]
    del df['yr']

    df['mfr'] = [x.split()[0] for x in df.name]
    df.loc[df.mfr=='chevy', 'mfr'] = 'chevrolet'
    df.loc[df.mfr=='chevroelt', 'mfr'] = 'chevrolet'
    df.loc[df.mfr=='maxda', 'mfr'] = 'mazda'
    df.loc[df.mfr=='mercedes-benz', 'mfr'] = 'mercedes'
    df.loc[df.mfr=='toyouta', 'mfr'] = 'toyota'
    df.loc[df.mfr=='vokswagen', 'mfr'] = 'volkswagen'
    df.loc[df.mfr=='vw', 'mfr'] = 'volkswagen'
    del df['name']

    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]
    quantileable = [x for x in continuous if len(df[x].unique()) > 20]

    return df, columns, discrete, continuous, quantileable