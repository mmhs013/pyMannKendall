"""
Created on 05 March 2018
Update on 28 May 2021
@author: Md. Manjurul Hussain Shourov
version: 1.4.2
Approach: Vectorisation
Citation: Hussain et al., (2019). pyMannKendall: a python package for non parametric Mann Kendall family of trend tests.. Journal of Open Source Software, 4(39), 1556, https://doi.org/10.21105/joss.01556
"""

from __future__ import division
import numpy as np
from scipy.stats import norm, rankdata
from collections import namedtuple


# Supporting Functions
# Data Preprocessing
def __preprocessing(x):
    x = np.asarray(x).astype(float)
    dim = x.ndim
    
    if dim == 1:
        c = 1
        
    elif dim == 2:
        (n, c) = x.shape
        
        if c == 1:
            dim = 1
            x = x.flatten()
         
    else:
        print('Please check your dataset.')
        
    return x, c

	
# Missing Values Analysis
def __missing_values_analysis(x, method = 'skip'):
    if method.lower() == 'skip':
        if x.ndim == 1:
            x = x[~np.isnan(x)]
            
        else:
            x = x[~np.isnan(x).any(axis=1)]
    
    n = len(x)
    
    return x, n

	
# ACF Calculation
def __acf(x, nlags):
    y = x - x.mean()
    n = len(x)
    d = n * np.ones(2 * n - 1)
    
    acov = (np.correlate(y, y, 'full') / d)[n - 1:]
    
    if acov[0] != 0 :
        return acov[:nlags+1]/acov[0]
    else :
        return acov[:nlags+1]     


# vectorization approach to calculate mk score, S
def __mk_score(x, n):
    s = 0

    demo = np.ones(n) 
    for k in range(n-1):
        s = s + np.sum(demo[k+1:n][x[k+1:n] > x[k]]) - np.sum(demo[k+1:n][x[k+1:n] < x[k]])
        
    return s

	
# original Mann-Kendal's variance S calculation
def __variance_s(x, n):
    # calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # calculate the var(s)
    if n == g:            # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18
        
    else:                 # there are some ties in data
        tp = np.zeros(unique_x.shape)
        demo = np.ones(n)
        
        for i in range(g):
            tp[i] = np.sum(demo[x == unique_x[i]])
            
        var_s = (n*(n-1)*(2*n+5) - np.sum(tp*(tp-1)*(2*tp+5)))/18
        
    return var_s


# standardized test statistic Z
def __z_score(s, var_s):
    if s > 0:
        z = (s - 1)/np.sqrt(var_s)
    elif s == 0:
        z = 0
    elif s < 0:
        z = (s + 1)/np.sqrt(var_s)
    
    return z


# calculate the p_value
def __p_value(z, alpha):
    # two tail test
    p = 2*(1-norm.cdf(abs(z)))  
    h = abs(z) > norm.ppf(1-alpha/2)

    if (z < 0) and h:
        trend = 'decreasing'
    elif (z > 0) and h:
        trend = 'increasing'
    else:
        trend = 'no trend'
    
    return p, h, trend


def __R(x):
    n = len(x)
    R = []
    
    for j in range(n):
        i = np.arange(n)
        s = np.sum(np.sign(x[j] - x[i]))
        R.extend([(n + 1 + s)/2])
    
    return np.asarray(R)


def __K(x,z):
    n = len(x)
    K = 0
    
    for i in range(n-1):
        j = np.arange(i,n)
        K = K + np.sum(np.sign((x[j] - x[i]) * (z[j] - z[i])))
    
    return K

	
# Original Sens Estimator
def __sens_estimator(x):
    idx = 0
    n = len(x)
    d = np.ones(int(n*(n-1)/2))

    for i in range(n-1):
        j = np.arange(i+1,n)
        d[idx : idx + len(j)] = (x[j] - x[i]) / (j - i)
        idx = idx + len(j)
        
    return d


def sens_slope(x):
    """
    This method proposed by Theil (1950) and Sen (1968) to estimate the magnitude of the monotonic trend. Intercept calculated using Conover, W.J. (1980) method.
    Input:
        x:   a one dimensional vector (list, numpy array or pandas series) data
    Output:
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(120)
      >>> slope,intercept = mk.sens_slope(x)
    """
    res = namedtuple('Sens_Slope_Test', ['slope','intercept'])
    x, c = __preprocessing(x)
#     x, n = __missing_values_analysis(x, method = 'skip')
    n = len(x)
    slope = np.nanmedian(__sens_estimator(x))
    intercept = np.nanmedian(x) - np.median(np.arange(n)[~np.isnan(x.flatten())]) * slope  # or median(x) - (n-1)/2 *slope
    
    return res(slope, intercept)


def seasonal_sens_slope(x_old, period=12):
    """
    This method proposed by Hipel (1994) to estimate the magnitude of the monotonic trend, when data has seasonal effects. Intercept calculated using Conover, W.J. (1980) method.
    Input:
        x:   a vector (list, numpy array or pandas series) data
		period: seasonal cycle. For monthly data it is 12, weekly data it is 52 (12 is the default)
    Output:
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line, where full period cycle consider as unit time step
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(120)
      >>> slope,intercept = mk.seasonal_sens_slope(x, 12)
    """
    res = namedtuple('Seasonal_Sens_Slope_Test', ['slope','intercept'])
    x, c = __preprocessing(x_old)
    n = len(x)
    
    if x.ndim == 1:
        if np.mod(n,period) != 0:
            x = np.pad(x,(0,period - np.mod(n,period)), 'constant', constant_values=(np.nan,))

        x = x.reshape(int(len(x)/period),period)
    
#     x, n = __missing_values_analysis(x, method = 'skip')
    d = []
    
    for i in range(period):
        d.extend(__sens_estimator(x[:,i]))
        
    slope = np.nanmedian(np.asarray(d))
    intercept = np.nanmedian(x_old) - np.median(np.arange(x_old.size)[~np.isnan(x_old.flatten())]) / period * slope
    
    return res(slope, intercept)

	
def original_test(x_old, alpha = 0.05):
    """
    This function checks the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert 1987).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
	  >>> import numpy as np
      >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.original_test(x,0.05)
    """
    res = namedtuple('Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    s = __mk_score(x, n)
    var_s = __variance_s(x, n)
    Tau = s/(.5*n*(n-1))
    
    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)
    slope, intercept = sens_slope(x_old)

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)

def hamed_rao_modification_test(x_old, alpha = 0.05, lag=None):
    """
    This function checks the Modified Mann-Kendall (MK) test using Hamed and Rao (1998) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        lag: No. of First Significant Lags (default None, You can use 3 for considering first 3 lags, which also proposed by Hamed and Rao(1998))
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.hamed_rao_modification_test(x,0.05)
    """
    res = namedtuple('Modified_Mann_Kendall_Test_Hamed_Rao_Approach', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    s = __mk_score(x, n)
    var_s = __variance_s(x, n)
    Tau = s/(.5*n*(n-1))

    # Hamed and Rao (1998) variance correction
    if lag is None:
        lag = n
    else:
        lag = lag + 1
        
    # detrending
    # x_detrend = x - np.multiply(range(1,n+1), np.median(x))
    slope, intercept = sens_slope(x_old)
    x_detrend = x - np.arange(1,n+1) * slope
    I = rankdata(x_detrend)
    
    # account for autocorrelation
    acf_1 = __acf(I, nlags=lag-1)
    interval = norm.ppf(1 - alpha / 2) / np.sqrt(n)
    upper_bound = 0 + interval
    lower_bound = 0 - interval

    sni = 0
    for i in range(1,lag):
        if (acf_1[i] <= upper_bound and acf_1[i] >= lower_bound):
            sni = sni
        else:
            sni += (n-i) * (n-i-1) * (n-i-2) * acf_1[i]
            
    n_ns = 1 + (2 / (n * (n-1) * (n-2))) * abs(sni)
    var_s = var_s * n_ns
    
    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)
        
    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)

def yue_wang_modification_test(x_old, alpha = 0.05, lag=None):
    """
    Input: This function checks the Modified Mann-Kendall (MK) test using Yue and Wang (2004) method.
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        lag: No. of First Significant Lags (default None, You can use 1 for considering first 1 lags, which also proposed by Yue and Wang (2004))
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.yue_wang_modification_test(x,0.05)
    """
    res = namedtuple('Modified_Mann_Kendall_Test_Yue_Wang_Approach', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    s = __mk_score(x, n)
    var_s = __variance_s(x, n)
    Tau = s/(.5*n*(n-1))
    
    # Yue and Wang (2004) variance correction
    if lag is None:
        lag = n
    else:
        lag = lag + 1

    # detrending
    slope, intercept = sens_slope(x_old)
    x_detrend = x - np.arange(1,n+1) * slope
    
    # account for autocorrelation
    acf_1 = __acf(x_detrend, nlags=lag-1)
    idx = np.arange(1,lag)
    sni = np.sum((1 - idx/n) * acf_1[idx])
    
    n_ns = 1 + 2 * sni
    var_s = var_s * n_ns

    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)

def pre_whitening_modification_test(x_old, alpha = 0.05):
    """
    This function checks the Modified Mann-Kendall (MK) test using Pre-Whitening method proposed by Yue and Wang (2002).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.pre_whitening_modification_test(x,0.05)
    """
    res = namedtuple('Modified_Mann_Kendall_Test_PreWhitening_Approach', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    # PreWhitening
    acf_1 = __acf(x, nlags=1)[1]
    a = range(0, n-1)
    b = range(1, n)
    x = x[b] - x[a]*acf_1
    n = len(x)
    
    s = __mk_score(x, n)
    var_s = __variance_s(x, n)
    Tau = s/(.5*n*(n-1))
    
    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)
    slope, intercept = sens_slope(x_old)
    
    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)

def trend_free_pre_whitening_modification_test(x_old, alpha = 0.05):
    """
    This function checks the Modified Mann-Kendall (MK) test using the trend-free Pre-Whitening method proposed by Yue and Wang (2002).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.trend_free_pre_whitening_modification_test(x,0.05)
    """
    res = namedtuple('Modified_Mann_Kendall_Test_Trend_Free_PreWhitening_Approach', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    # detrending
    slope, intercept = sens_slope(x_old)
    x_detrend = x - np.arange(1,n+1) * slope
    
    # PreWhitening
    acf_1 = __acf(x_detrend, nlags=1)[1]
    a = range(0, n-1)
    b = range(1, n)
    x = x_detrend[b] - x_detrend[a]*acf_1

    n = len(x)
    x = x + np.arange(1,n+1) * slope
    
    s = __mk_score(x, n)
    var_s = __variance_s(x, n)
    Tau = s/(.5*n*(n-1))
    
    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)
    slope, intercept = sens_slope(x_old)
    
    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def multivariate_test(x_old, alpha = 0.05):
    """
    This function checks the Multivariate Mann-Kendall (MK) test, which is originally proposed by R. M. Hirsch and J. R. Slack (1984) for the seasonal Mann-Kendall test. Later this method also used Helsel (2006) for Regional Mann-Kendall test.
    Input:
        x: a matrix of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.multivariate_test(x,0.05)
    """
    res = namedtuple('Multivariate_Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    s = 0
    var_s = 0
    denom = 0
    
    x, c = __preprocessing(x_old)
#     x, n = __missing_values_analysis(x, method = 'skip')  # It makes all column at the same size

    for i in range(c):
        if c == 1:
            x_new, n = __missing_values_analysis(x, method = 'skip')  # It makes all column at deferent size
        else:
            x_new, n = __missing_values_analysis(x[:,i], method = 'skip')  # It makes all column at deferent size

        s = s + __mk_score(x_new, n)
        var_s = var_s + __variance_s(x_new, n)
        denom = denom + (.5*n*(n-1))
              
    Tau = s/denom
    
    z = __z_score(s, var_s)
    p, h, trend = __p_value(z, alpha)

    slope, intercept = seasonal_sens_slope(x_old, period = c)
    
    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def seasonal_test(x_old, period = 12, alpha = 0.05):
    """
    This function checks the  Seasonal Mann-Kendall (MK) test (Hirsch, R. M., Slack, J. R. 1984).
    Input:
        x:   a vector of data
        period: seasonal cycle. For monthly data it is 12, weekly data it is 52 (12 is the default)
        alpha: significance level (0.05 is the default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line, where full period cycle consider as unit time step
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.seasonal_test(x,0.05)
    """
    res = namedtuple('Seasonal_Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)
    n = len(x)
    
    if x.ndim == 1:
        if np.mod(n,period) != 0:
            x = np.pad(x,(0,period - np.mod(n,period)), 'constant', constant_values=(np.nan,))

        x = x.reshape(int(len(x)/period),period)
    
    trend, h, p, z, Tau, s, var_s, slope, intercept = multivariate_test(x, alpha = alpha)

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def regional_test(x_old, alpha = 0.05):
    """
    This function checks the Regional Mann-Kendall (MK) test (Helsel 2006).
    Input:
        x:   a matrix of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000,5)  # here consider 5 station/location where every station have 1000 data
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.regional_test(x,0.05)
    """
    res = namedtuple('Regional_Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    
    trend, h, p, z, Tau, s, var_s, slope, intercept = multivariate_test(x_old)
    
    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def correlated_multivariate_test(x_old, alpha = 0.05):
    """
    This function checks the Correlated Multivariate Mann-Kendall (MK) test (Libiseller and Grimvall (2002)).
    Input:
        x:   a matrix of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000, 2)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.correlated_multivariate_test(x,0.05)
    """
    res = namedtuple('Correlated_Multivariate_Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    s = 0
    denom = 0
    
    for i in range(c):
        s = s + __mk_score(x[:,i], n)
        denom = denom + (.5*n*(n-1))
 
    Tau = s/denom

    Gamma = np.ones([c,c])

    for i in range(1,c):
        for j in range(i):
            k = __K(x[:,i], x[:,j])
            ri = __R(x[:,i])
            rj = __R(x[:,j])
            Gamma[i,j] = (k + 4 * np.sum(ri * rj) - n*(n+1)**2)/3
            Gamma[j,i] = Gamma[i,j]

    for i in range(c):
        k = __K(x[:,i], x[:,i])
        ri = __R(x[:,i])
        rj = __R(x[:,i])
        Gamma[i,i] = (k + 4 * np.sum(ri * rj) - n*(n+1)**2)/3
    
    
    var_s = np.sum(Gamma)
    
    z = s / np.sqrt(var_s)

    p, h, trend = __p_value(z, alpha)
    slope, intercept = seasonal_sens_slope(x_old, period=c)

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def correlated_seasonal_test(x_old, period = 12 ,alpha = 0.05):
    """
    This function checks the Correlated Seasonal Mann-Kendall (MK) test (Hipel [1994] ).
    Input:
        x:   a matrix of data
		period: seasonal cycle. For monthly data it is 12, weekly data it is 52 (12 is default)
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
        intercept: intercept of Kendall-Theil Robust Line, where full period cycle consider as unit time step
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.correlated_seasonal_test(x,0.05)
    """
    res = namedtuple('Correlated_Seasonal_Mann_Kendall_test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    x, c = __preprocessing(x_old)

    n = len(x)
    
    if x.ndim == 1:
        if np.mod(n,period) != 0:
            x = np.pad(x,(0,period - np.mod(n,period)), 'constant', constant_values=(np.nan,))

        x = x.reshape(int(len(x)/period),period)
    
    trend, h, p, z, Tau, s, var_s, slope, intercept = correlated_multivariate_test(x)

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)


def partial_test(x_old, alpha = 0.05):
    """
    This function checks the Partial Mann-Kendall (MK) test (Libiseller and Grimvall (2002)).
    Input:
        x: a matrix with 2 columns
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: Theil-Sen estimator/slope
    Examples
    --------
      >>> import numpy as np
	  >>> import pymannkendall as mk
      >>> x = np.random.rand(1000, 2)
      >>> trend,h,p,z,tau,s,var_s,slope,intercept = mk.partial_test(x,0.05)
    """
    res = namedtuple('Partial_Mann_Kendall_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'])
    
    x_proc, c = __preprocessing(x_old)
    x_proc, n = __missing_values_analysis(x_proc, method = 'skip')
    
    if c != 2:
        raise ValueError('Partial Mann Kendall test required two parameters/columns. Here column no ' + str(c) + ' is not equal to 2.')
    
    x = x_proc[:,0]
    y = x_proc[:,1]
    
    x_score = __mk_score(x, n)
    y_score = __mk_score(y, n)
    
    k = __K(x, y)
    rx = __R(x)
    ry = __R(y)
    
    sigma = (k + 4 * np.sum(rx * ry) - n*(n+1)**2)/3
    rho = sigma / (n*(n-1)*(2*n+5)/18)
    
    s = x_score - rho * y_score
    var_s = (1 - rho**2) * (n*(n-1)*(2*n+5))/18
    
    Tau = x_score/(.5*n*(n-1))
    
    z = s / np.sqrt(var_s)

    p, h, trend = __p_value(z, alpha)
    slope, intercept = sens_slope(x_old[:,0])

    return res(trend, h, p, z, Tau, s, var_s, slope, intercept)
