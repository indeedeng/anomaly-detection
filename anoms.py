import numpy as np
from pyloess import stl
from scipy.stats import t
from pandas import Series
from math import floor
import logging

logger = logging.getLogger('indeed.anoms')


def detect_anoms(x, period, max_anoms=0.10, alpha=0.05, direction='both', longterm_period=None, only_last=False,
                 threshold=None, e_value=False):
    if longterm_period is None:
        longterm_period = len(x)
    ret = set()
    if e_value:
        e_values = [None] * len(x)  # To keep the expected values when e_value is set.
    for period_start in xrange(0, len(x), longterm_period):
        period_end = min(len(x), period_start + longterm_period)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Start to process longterm period: period_start=%s, period_end=%s" %
                         (period_start, period_end))
        if only_last and period_end < len(x):
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("only_last is True. Skip longterm periods before the last one.")
            continue
        if period_end - period_start < longterm_period:
            period_start = period_end - longterm_period
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("The last longterm period doesn't contain enough length of data. "
                             "Adjusted the starting index. period_start=%s, period_end=%s" % (period_start, period_end))
        period_x = x[period_start:period_end]
        # parameters are copied from R's stl()
        stl_ret = stl(period_x, np=period, ns=len(period_x) * 10 + 1, isdeg=0, robust=True, ni=1, no=15)
        seasons = stl_ret['seasonal']
        if e_value:
            trends = stl_ret['trend']
            for i in range(0, len(period_x)):
                if e_values[period_start + i] is None:
                    e_values[period_start + i] = floor(seasons[i] + trends[i])
        median = np.median(period_x)
        resid = [period_x[i] - seasons[i] - median for i in range(0, len(period_x))]
        max_anom_num = max(1, int(len(period_x) * max_anoms))
        anom_index = _esd(resid, max_anom_num, alpha, direction=direction)
        for anom_i in anom_index:
            ret.add(period_start + anom_i)
        if threshold:
            period_maxs = []
            for i in xrange(0, len(period_x), period):
                period_maxs.append(max(period_x[i: min(len(period_x), i + period)]))
            if threshold == 'med_max':
                thresh = np.median(period_maxs)
            elif threshold == 'p95':
                thresh = np.percentile(period_maxs, 95)
            elif threshold == 'p99':
                thresh = np.percentile(period_maxs, 99)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("threshold is True. threshold=%s, thresh=%s" % (threshold, thresh))
            ret = set(filter(lambda index: x[index] >= thresh, ret))
        if only_last:
            last_period_start = len(x) - period
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("only_last is True. Will remove all anomalies before index %s." % last_period_start)
            ret = set(filter(lambda value: value > last_period_start, ret))
    ret = sorted(ret)
    if e_value:
        return ret, map(lambda i: e_values[i], ret)
    else:
        return ret


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
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("%s/%s outlier. median=%s, mad=%s, r_idx=%s, r=%s, crit=%s, lam=%s" %
                         (i, max_outlier, median, mad, r_idx, r, crit, lam))
        if r > lam:
            outlier_index.append(r_idx)
            x.drop(r_idx, inplace=True)
        else:
            break
    return outlier_index
