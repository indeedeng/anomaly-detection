from edm import edm_multi, edm_x, edm_tail, edm_percent
import numpy as np
import logging

logger = logging.getLogger("indeed.breakout")

_EDM_TAIL_QUANT = 0.5


def detect_breakout(z, min_size=30, method='amoc', alpha=2, exact=True, sig_level=0.05, nperm=0,
                    degree=1, beta=None, percent=None):
    """
    Breakout Detector: Energy Divisive with Medians
    A technique for robustly, i.e., in the presence of anomalies, detecting single or multiple change points in
    univariate time series.
    :param z: list of floats. The input time series.
    :param min_size: int. The minimum number of observations between change points.
    :param method: string. Method must be one of either 'amoc' (At Most One Change) or
                   'multi' (Multiple Changes). For 'amoc' at most one change point location will be returned.
    :param alpha: float in (0, 2]. For 'amoc' method. The alpha parameter used to weight the distance
                  between observations.
    :param exact: boolean. For 'amoc' method. True to use truemedians, False to use approximate medians
                           when determining change points.
    :param sig_level: float in (0, 1). For 'amoc' method. Once a change point is found its statistical significance is
                      determined through a hypothesis test. This is the significance.
    :param nperm: int >= 0. For 'amoc' method. The number of permutations to perform in order to obtain an approximate
                  p-value. If 0 then then permutation test is not performed.
    :param degree: int, can take the values 0, 1 or 2. For 'multi' method. The degree of the penalization polynomial.
    :param beta: float. For 'multi' method. Used to further control the amount of penalization.
    :param percent: float. For 'multi' method. This value specifies the minimum percent change in the goodness of fit
                    statistic to consider adding an additional change point.
    :return: list of int, containing the index of change points.
    """
    if not isinstance(min_size, int) or min_size < 2:
        raise ValueError("min_size must be an int >= 2.")
    if method == 'amoc':
        multi = False
        if alpha > 2 or alpha <= 0:
            raise ValueError("alpha must be in the interval (0, 2]")
        if sig_level <= 0 or sig_level >= 1:
            raise ValueError("sig_level must be in interval (0, 1)")
        if not isinstance(nperm, int) or nperm < 0:
            raise ValueError("nperm must be an int greater than 0.")
    elif method == 'multi':
        multi = True
        if degree not in [0, 1, 2]:
            raise ValueError("degree must be 0, 1 or 2.")
        if beta is None and percent is None:
            raise ValueError("beta and percent can not be both None.")
    else:
        raise ValueError("method must be 'amoc' or 'multi'")
    for value in z:
        if np.isnan(value):
            raise ValueError("data contains NaN.")
    if not z:
        return []
    z_max = max(z)
    z_min = min(z)
    distance = z_max - z_min
    if distance == 0:
        return []
    z = [(value - z_min) / distance for value in z]
    if not multi:
        if exact:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("calling edm_x")
            ret, stat = edm_x(z, min_size, alpha)
        else:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("calling edm_tail")
            ret, stat = edm_tail(z, min_size, alpha, _EDM_TAIL_QUANT)
        if nperm == 0:
            ret_list = [ret]
        else:
            over = 1
            for i in range(0, nperm):
                z_perm = list(np.random.permutation(z))
                if exact:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug("calling edm_x for nperm %s" % i)
                    _, stat_perm = edm_x(z_perm, min_size, alpha)
                else:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug("calling edm_tail for nperm %s" % i)
                    _, stat_perm = edm_tail(z_perm, min_size, alpha, _EDM_TAIL_QUANT)
                if stat_perm > stat:
                    over += 1
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug("over=%s, stat_perm=%s, stat=%s" % (over, stat_perm, stat))
            p_val = float(over) / (nperm + 1)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("over=%s, p_val=%s" % (over, p_val))
            if p_val > sig_level:
                ret_list = []
            else:
                ret_list = [ret]
    else:
        if beta is None:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("calling edm_percent")
            ret_list = edm_percent(z, min_size, percent, degree)
        else:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("calling edm_multi")
            ret_list = edm_multi(z, min_size, beta, degree)
    return ret_list
