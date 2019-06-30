# pyMannKendall
[![Build Status](https://travis-ci.org/mmhs013/pyMannKendall.svg?branch=master)](https://travis-ci.org/mmhs013/pyMannKendall)
[![PyPI](https://img.shields.io/pypi/v/pymannkendall.svg)](https://pypi.org/project/pymannkendall/)
[![PyPI - License](https://img.shields.io/pypi/l/pymannkendall.svg)](https://pypi.org/project/pymannkendall/)
[![PyPI - Status](https://img.shields.io/pypi/status/pymannkendall.svg)](https://pypi.org/project/pymannkendall/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pymannkendall.svg)](https://pypi.org/project/pymannkendall/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymannkendall.svg)](https://pypi.org/project/pymannkendall/)


`pyMannkendal` is a pure Python implementation of non-parametric Mann Kendall trend analysis. Currently, this package has 11 Mann-Kendall Tests and 2 sen's slope estimator function. Brief description of functions are below:

1.	**Original Mann Kendall test (*original_test*):** Original Mann Kendall test is a nonparametric test, which does not consider serial correlation or seasonal effects.

2.	**Hamed and Rao Modified MK Test (*hamed_rao_modification_test*):** This modified MK test proposed by Hamed and Rao (1998) to address serial autocorrelation issues. (Their) They suggested variance correction approach to improve trend analysis. User can consider first n significant lag by insert lag number in this function. By default, it considered all significant lags.

3.	**Yue and Wang Modified MK Test (*yue_wang_modification_test*):** This is also a variance correction method for considered serial autocorrelation proposed by Yue, S., & Wang, C. Y. (2004). User can also set their desired significant n lags for the calculation.

4.	**Modified MK test using Pre-Whitening method (*pre_whitening_modification_test*):** This test suggested by Yue and Wang (2002) to using Pre-Whitening the time series prior to the application of trend test.

5.	**Modified MK test using Trend free Pre-Whitening method (*trend_free_pre_whitening_modification_test*):** This test also proposed by Yue and Wang (2002) to remove trend component and then Pre-Whitening the time series prior to application of trend test.

6.	**Multivariate MK Test (*multivariate_test*):** This is an MK test for multiple parameters proposed by Hirsch (1982). Actually, he used this method for seasonal mk test, where he considered every month is a parameter.

7.	**Seasonal MK Test (*seasonal_test*):** For seasonal time series data, Hirsch, R.M., Slack, J.R. and Smith, R.A. (1982) proposed this test to calculate the seasonal trend.

8.	**Regional MK Test (*regional_test*):** Based on Hirsch (1982) proposed seasonal mk test, Helsel, D.R. and Frans, L.M., (2006) suggest regional mk test to calculate overall trend a regional scale.

9.	**Correlated Multivariate MK Test (*correlated_multivariate_test*):** This multivariate mk test proposed by Hipel (1994) for when parameters are correlated.

10.	**Correlated Seasonal MK Test (*correlated_seasonal_test*):** This method proposed by Hipel (1994) used, when time series significantly correlated with the preceding one or more months/seasons.

11.	**Partial MK Test (*partial_test*):** In a real event, many factors are affecting the main studied response parameter, which can bias the trend results. To overcome this problem, Libiseller (2002) proposed this partial mk test. It required two parameters as input, where, one is response parameter and other is an independent parameter.

12.	**Theil-sen's Slope Estimator (*sens_slope*):** This method proposed by Theil (1950) and Sen (1968) to estimate the magnitude of the monotonic trend.

13.	**Seasonal sen's Slope Estimator (*seasonal_sens_slope*):** This method proposed by Hipel (1994) to estimate the magnitude of the monotonic trend, when data has seasonal effects.

# Function details:

All Mann-kendall test functions has almost similer input parameters. Those are:

- **x**:   a vector of data
- **alpha**: significance level (0.05 default)
- **lag**: No. of First Significant Lags (Only available in hamed_rao_modification_test and yue_wang_modification_test)
- **period**: seasonal cycle. For monthly data it is 12, weekly data it is 52 (Only available in seasonal tests)

And all Mann-kendall tests return a named tuple which contained:

- **trend**: tells the trend (increasing, decreasing or no trend)
- **h**: True (if trend is present) or False (if trend is absence)
- **p**: p value of the significance test
- **z**: normalized test statistics
- **Tau**: Kendall Tau
- **s**: Mann-Kendal's score
- **var_s**: Variance S
- **slope**: sen's slope

sen's slope function required data vector. seasonal sen's slope also has optional input period, which by default value is 12. Both sen's slope function return only slope value.

# Installation

You can install pyMannKendall using pip.

```python
pip install pymannkendall
```

Or you can clone the repo and install it:

```bash
git clone https://github.com/mmhs013/pymannkendall
cd pymannkendall
python setup.py install
```

# Usage

Here an example of `pyMannKendall` usage:
```python
import numpy as np
import pymannkendall as mk

# Data generation for analysis
data = np.random.rand(360,1)

result = mk.original_test(data)
print(result)
```
Output are like this:
```python
Mann_Kendall_Test(trend='no trend', h=False, p=0.9535148145990886, z=0.05829353811789905, Tau=0.002073661405137728, s=134.0, var_s=5205500.0, slope=8.408683160625719e-06)
```
Whereas, the output is a named tuple, so you can call by name for specific result:
```python
print(result.slope)
```
or, you can directly unpack your results like this:
```python
trend, h, p, z, Tau, s, var_s, slope = mk.original_test(data)
```
## Contributions

`pyMannKendall` is a community project and welcomes contributions. Additional information can be found in the [contribution guidelines](https://github.com/mmhs013/pyMannKendall/blob/master/CONTRIBUTING.md)


## Code of Conduct

`pyMannKendall` wishes to maintain a positive community. Additional details can be found in the [Code of Conduct](https://github.com/mmhs013/pyMannKendall/blob/master/CODE_OF_CONDUCT.md)


