import numpy as np
from pyloess import stl
from scipy.stats import t
from pandas import Series


def detect_anoms(x, peroid, max_anoms=0.10, alpha=0.05, direction='both', longterm_period=None):
    if longterm_period is None:
        longterm_period = len(x)
    ret = []
    for period_end in xrange(len(x), 0, -longterm_period):
        period_start = max(0, period_end - longterm_period)
        period_x = x[period_start:period_end]
        # parameters are copied from R's stl()
        stl_ret = stl(period_x, np=peroid, ns=len(period_x) * 10 + 1, isdeg=0, robust=True, ni=1, no=15)
        seasons = stl_ret['seasonal']
        median = np.median(period_x)
        resid = [period_x[i] - seasons[i] - median for i in range(0, len(period_x))]
        max_anom_num = max(1, int(len(period_x) * max_anoms))
        anom_index = _esd(resid, max_anom_num, alpha, direction=direction)
        for anom_i in anom_index:
            ret.append(period_start + anom_i)
    return sorted(ret)


_MAD_CONSTANT = 1.4826  # a magic number copied from R's mad() function


def _esd(x, max_outlier, alpha, direction='both'):
    x = Series(x)
    n = len(x)
    outlier_index = []
    for i in range(1, max_outlier + 1):
        median = x.median()
        mad = np.median([abs(value - median) for value in x]) * _MAD_CONSTANT
        if mad == 0:
            break
        if direction == 'both':
            ares = x.map(lambda value: abs(value - median) / mad)
        elif direction == 'pos':
            ares = x.map(lambda value: (value - median) / mad)
        elif direction == 'neg':
            ares = x.map(lambda value: (median - value) / mad)
        r_idx = ares.idxmax()
        r = ares[r_idx]
        if direction == 'both':
            p = 1.0 - alpha / (2 * (n - i + 1))
        else:
            p = 1.0 - alpha / (n - i + 1)
        crit = t.ppf(p, n-i-1)
        lam = (n-i)*crit / np.sqrt((n-i-1+crit**2) * (n-i+1))
        if r > lam:
            outlier_index.append(r_idx)
            x.drop(r_idx, inplace=True)
        else:
            break
    return outlier_index
