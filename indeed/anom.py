import numpy as np
import statsmodels.tsa.seasonal as seasonal
from PyAstronomy import pyasl
from scipy.stats import t
from pandas import Series


def detect_anoms(x, peroid, max_anoms=0.10, alpha=0.05, direction='both',
                 longterm_period=None):
    if longterm_period is None:
        longterm_period = len(x)
    ret = []
    for period_end in xrange(len(x), 0, -longterm_period):
        period_start = max(0, period_end - longterm_period)
        period_x = x[period_start:period_end]
        stl_res = seasonal.seasonal_decompose(period_x, freq=peroid)
        seasons = stl_res.seasonal
        median = np.median(period_x)
        resid = [period_x[i] - seasons[i] - median for i in range(0, len(period_x))]
        max_anom_num = max(1, int(len(period_x) * max_anoms))
        anom_index = _esd(resid, max_anom_num, alpha, direction=direction)
        for anom_i in anom_index:
            ret.append(period_start + anom_i)
    return ret


def _esd(x, max_outlier, alpha, direction='both'):
    x = Series(x)
    n = len(x)
    outlier_index = []
    for i in range(1, max_outlier + 1):
        median = x.median()
        mad = np.median([abs(value - median) for value in x])
        if mad == 0:
            break
        if direction == 'both':
            ares = x.map(lambda value: abs(value - median) / mad)
        elif direction == 'pos':
            ares = x.map(lambda value: (value - median) / mad)
        elif direction == 'neg':
            ares = x.map(lambda value: (median - value) / mad)
        r_idx = ares.idxmax()
        r = ares.max()
        if direction == 'both':
            p = 1.0 - alpha / (2 * (n - i + 1))
        else:
            p = 1.0 - alpha / (n - i + 1)
        crit = t.ppf(p, n-i-1)
        lam = (n-i)*crit / np.sqrt((n-i-1+crit**2) * (n-i+1))
        if r > lam:
            outlier_index.append(r_idx)
            x = x.drop(r_idx)
        else:
            break
    return outlier_index
