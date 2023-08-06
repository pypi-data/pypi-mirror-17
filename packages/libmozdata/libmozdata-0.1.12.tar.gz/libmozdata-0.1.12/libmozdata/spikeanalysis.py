# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import scipy.stats as stats
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import ticker
from . import utils


def ma(x, win):
    """Compute the moving average of x with a window equal to win

    Args:
        x (numpy.array): data
        win (int): window

    Returns:
        numpy.array: the smoothed data
    """
    y = np.ones(win, dtype=np.float64)
    i = win - 1
    _x = np.convolve(x, y, mode='full')[:-i]
    _x[1:i] = _x[1:i] / np.arange(2., win, dtype=np.float64)
    _x[i:] = _x[i:] / float(win)

    return _x


def normalize(x):
    """Normalize data to have them in interval [0; 1]

    Args:
        x (numpy.array): data

    Returns:
        numpy.array: the normalized data
    """
    m = np.nanmin(x)
    M = np.nanmax(x)
    if m != M:
        return (x - m) / (M - m)
    else:
        return x / m


def __get_grubb_lambda(n, alpha):
    """Get the value to use for the Grubb's test
       http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h1.htm

    Args:
        n (int): the number of elements in the sample
        alpha (float): the signifiance level

    Returns:
        float: the critical value to use
    """
    n = float(n)
    p = alpha / (2. * n)
    t = np.abs(stats.t.ppf(p, n - 2.))
    l = (n - 1.) * t / np.sqrt((n - 2. + t ** 2) * n)

    return l


def __get_pd_median(data, c=stats.norm.ppf(0.75)):
    """Get the median and the mad of data

    Args:
        data (numpy.ndarray): the data

    Returns:
        float, float: the median and the mad
    """
    p = np.nanmedian(data)
    d = np.nanmedian(np.abs(data - p)) / c  # d is the MAD

    return p, d


def __get_pd_mean(data, c=1.):
    """Get the mean and the standard deviation of data

    Args:
        data (numpy.ndarray): the data

    Returns:
        float, float: the mean and the standard deviation
    """
    p = np.nanmean(data)
    d = np.nanstd(data) / c

    return p, d


def get_spikes(data, alpha=0.05, win=-1, threshold_up=-float('Inf'), threshold_down=+float('Inf'), method='median', plot=False):
    """Get the spikes in data.
       The Grubb's test is applyed to determinate if a value is an outlier or not (http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h1.htm)

    Args:
        data (numpy.ndarray): the data
        alpha (float): the signifiance level
        win (int): the size of the window to use to compute the parameters
        threshold_up (float): the min value to say that a spike is a spike
        threshold_down (float): the min value to say that a spike is a spike
        method (str): 'median' or 'mean'
        plot (Bool): True if a plot is wanted

    Returns:
        list[int], list[int]: the index of the spikes (up and down)
    """

    # TODO:
    # It could be interesting to remove the noise in using wavelets.
    # And maybe we could use them to detect the outliers too.

    if isinstance(data, dict):
        data = [i[1] for i in sorted(data.items(), key=lambda p: p[0])]
    if isinstance(data, list):
        data = np.asarray(data, dtype=np.float64)

    fn = __get_pd_median if method == 'median' else __get_pd_mean
    _data = np.copy(data)
    NaN = float('nan')
    spikes_up = []
    spikes_down = []

    for i in range(3, len(data) + 1):
        start = max(0, i - win) if win > 0 else 0
        d = _data[start:i]
        x = d[-1]
        N = d.size - np.isnan(d).sum()  # number of non NaN values
        m, e = fn(d)
        l = __get_grubb_lambda(N, alpha)
        th = l * e
        if abs(x - m) > th:  # Grubb's test
            _data[i - 1] = NaN  # to ignore this outlier in the future
            if x > m + th and x >= threshold_up and x > data[i - 2]:
                spikes_up.append(i - 1)
            elif x < m - th and x <= threshold_down and x < data[i - 2]:
                spikes_down.append(i - 1)

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        X = np.arange(len(data))
        Y = data
        ax.plot(X, Y, color='blue')
        if spikes_up:
            ax.plot(X[spikes_up], Y[spikes_up], 'ro', color='red')
        if spikes_down:
            ax.plot(X[spikes_down], Y[spikes_down], 'ro', color='green')
        plt.show()

    return spikes_up, spikes_down


def is_spiking(data, alpha=0.05, win=-1, threshold_up=-float('Inf'), threshold_down=+float('Inf'), method='median', plot=False):
    """Check if the last value is a spike (up).

    Args:
        data (numpy.ndarray): the data
        alpha (float): the signifiance level
        win (int): the size of the window to use to compute the parameters
        threshold_up (float): the min value to say that a spike is a spike
        threshold_down (float): the min value to say that a spike is a spike
        method (str): 'median' or 'mean'
        plot (Bool): True if a plot is wanted

    Returns:
        Bool: True if the last value is a spike (up).
    """
    up, _ = get_spikes(data, alpha=alpha, win=win, threshold_up=threshold_up, threshold_down=threshold_down, method=method, plot=plot)
    return up and up[-1] == len(data) - 1


def is_spiking_ma(data, alpha=2.5, win=7, method='mean', plot=False):
    data = np.asarray(data, dtype=np.float64)
    fn = __get_pd_median if method == 'median' else __get_pd_mean
    NaN = float('nan')
    up = []
    down = []
    trend = ma(data, win)
    noise = data - trend
    noise = ma(noise, win)

    _noise = np.copy(noise) if plot else None

    for i in range(win, len(noise) + 1):
        if up and up[-1] == i - 2 and noise[i - 2] < noise[i - 1]:
            up.append(i - 1)
            noise[i - 1] = NaN
            continue
        elif down and down[-1] == i - 2 and noise[i - 2] > noise[i - 1]:
            down.append(i - 1)
            noise[i - 1] = NaN
            continue
        
        x = noise[:i]
        ax = np.abs(x)

        m, e = fn(ax)
        if np.abs(ax[-1] - m) > alpha * e:
            if x[-1] > 0:
                up.append(i - 1)
            elif x[-1] < 0:
                down.append(i - 1)
            
            if x[-1] != 0:    
                noise[i - 1] = NaN
                for j in range(i - 2, -1, -1):
                    if (x[-1] > 0 and x[j] < x[j + 1]) or (x[-1] < 0 and x[j] > x[j + 1]):
                        noise[j] = NaN
                    else:
                        break
        elif (up and up[-1] == i - 2) or (down and down[-1] == i - 2):
            noise[i - 1] = NaN

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1)
        x = np.arange(len(data))
        ax.plot(x, data, color='red')
        ax.plot(x, trend, color='blue')
        ax.plot(x[up], data[up], 'ro', color='green')
        ax.plot(x[down], data[down], 'ro', color='yellow')

        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x, _noise, color='red')
        ax.plot(x, noise, color='blue')
        ax.plot(x[up], _noise[up], 'ro', color='green')
        ax.plot(x[down], _noise[down], 'ro', color='yellow')

        plt.show()

    if up and up[-1] == len(data) - 1 and data[-1] > data[-2] and np.max(data[-win:]) == data[-1]:
        return 'up'
    elif down and down[-1] == len(data) - 1 and data[-1] < data[-2] and np.min(data[-win:]) == data[-1]:
        return 'down'
    else:
        return 'none'


def get_spikes_ma(data, alpha=2.5, win=7, method='mean', plot=False):
    original = data
    if isinstance(data, dict):
        data = np.asarray([float(i[1]) for i in sorted(data.items(), key=lambda p: p[0])], dtype=np.float64)
    if isinstance(data, list):
        data = np.asarray(data, dtype=np.float64)

    up = []
    down = []
    
    for i in range(win, len(data) + 1):
        print('%d on %d' % (i, len(data)))
        s = is_spiking_ma(data[:i], alpha=alpha, win=win, method=method)
        if s == 'up':
            up.append(i - 1)
        elif s == 'down':
            down.append(i - 1)

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        if isinstance(original, dict):
            labels = [i for i in sorted(original.keys())]
            if isinstance(labels[0], datetime):
                # take only the monday
                xlabels = []
                _labels = []
                for i in range(len(labels)):
                    d = labels[i]
                    if d.isocalendar()[2] == 1:  # we've a monday
                        xlabels.append(i)
                        _labels.append(utils.get_date_str(d))
                labels = _labels
                ax.xaxis.set_major_locator(ticker.FixedLocator(xlabels))
                #ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
                ax.xaxis.set_ticklabels(labels, rotation='vertical', fontsize=10)

        x = np.arange(len(original))
        ax.plot(x, data, color='red')
        ax.plot(x[up], data[up], 'ro', color='green')
        ax.plot(x[down], data[down], 'ro', color='yellow')

        plt.show()

    return up, down
