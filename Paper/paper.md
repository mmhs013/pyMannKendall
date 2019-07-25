---
title: 'pyMannKendall: a python package for non parametric Mann Kendall family of trend tests.'
tags:
  - mann kendall
  - modified mann kendall
  - sen's slope
authors:
 - name: Md. Manjurul Hussain
   orcid: 0000-0002-5361-0633
   affiliation: 1
 - name: Ishtiak Mahmud
   orcid: 0000-0002-4753-5403
   affiliation: 2   
affiliations:
 - name: Institute of Water and Flood Management, Bangladesh University of Engineering and Technology, Dhaka, Bangladesh
   index: 1
 - name: Shahjalal University of Science and Technology, Sylhet, Bangladesh
   index: 2
date: 30 June 2019
bibliography: paper.bib
---

# Summary

Trend analysis is one of the most important measurements in studying time series data. Both parametric and non-parametric tests are commonly used in trend analysis. Parametric tests require data to be independent and normally distributed. On the other hand, non-parametric trend tests require only that the data be independent and can tolerate outliers in the data [@hamed1998modified]. However, parametric tests are more powerful than nonparametric ones.

The Mann–Kendall trend test [@mann1945nonparametric; @kendall1975rank] is a widely used non-parametric tests to detect significant trends in time series. However, the original Mann-Kendall test didn't consider serial correlation or seasonality effects [@bari2016analysis; @hirsch1982techniques]. But, in many real situations, the observed data are autocorrelated and this autocorrelation will result in misinterpretation of trend tests results [@hamed1998modified; @cox1955some]. Contrariwise, water quality, hydrologic, as well as climatic and other natural time series also have seasonality. To overcome those limitations of original Mann-Kendall test, various modified Mann-Kendall test have been developed.

Again, Python is one of the widely used tools for data analysis. A large number of data analysis and research tools are also developed using Python. But, till now, there is no Mann-Kendall trend relation Python package available. ``pyMannKendall`` package fills this gap.

``pyMannKendall`` is written in pure Python and uses a vectorization approach to increase its performance. Currently, this package has 11 Mann-Kendall Tests and 2 Sen’s slope estimator functions. Brief description of the functions are below:

1.	**Original Mann-Kendall test (*original_test*):** Original Mann-Kendall test [@mann1945nonparametric; @kendall1975rank] is a nonparametric test, which does not consider serial correlation or seasonal effects.

2.	**Hamed and Rao Modified MK Test (*hamed_rao_modification_test*):** This modified MK test was proposed by @hamed1998modified to address serial autocorrelation issues. They suggested a variance correction approach to improve trend analysis. Users can consider first n significant lag by insert lag number in this function. By default, it considered all significant lags.

3.	**Yue and Wang Modified MK Test (*yue_wang_modification_test*):** This is also a variance correction method for considered serial autocorrelation proposed by @yue2004mann. Users can also set their desired significant number of lags for the calculation.

4.	**Modified MK test using Pre-Whitening method (*pre_whitening_modification_test*):** This test was suggested by @yue2002applicability to use Pre-Whitening the time series before the application of trend test.

5.	**Modified MK test using Trend free Pre-Whitening method (*trend_free_pre_whitening_modification_test*):** This test was also proposed by @yue2002influence to remove trend components and then Pre-Whitening the time series before application of trend test.

6.	**Multivariate MK Test (*multivariate_test*):** This is an MK test for multiple parameters proposed by @hirsch1982techniques. They used this method for seasonal MK tests, where they considered every month as a parameter.

7.	**Seasonal MK Test (*seasonal_test*):** For seasonal time series data, @hirsch1982techniques proposed this test to calculate the seasonal trend.

8.	**Regional MK Test (*regional_test*):** Based on the proposed seasonal MK test of @hirsch1982techniques, @helsel2006regional suggest a regional MK test to calculate the overall trend on a regional scale.

9.	**Correlated Multivariate MK Test (*correlated_multivariate_test*):** This multivariate MK test was proposed by @hipel1994time for where the parameters are correlated.

10.	**Correlated Seasonal MK Test (*correlated_seasonal_test*):** This method was proposed by @hipel1994time, for when time series significantly correlate with the preceding one or more months/seasons.

11.	**Partial MK Test (*partial_test*):** In a real event, many factors affect the main studied response parameter, which can bias the trend results. To overcome this problem, @libiseller2002performance proposed this partial mk test. It required two parameters as input, where one is the response parameter and other is an independent parameter.

12.	**Theil-sen's Slope Estimator (*sens_slope*):** This method was proposed by @theil1950rank and @sen1968estimates to estimate the magnitude of the monotonic trend.

13.	**Seasonal sen's Slope Estimator (*seasonal_sens_slope*):** This method was proposed by @hipel1994time to estimate the magnitude of the monotonic trend, when data has seasonal effects.


`pyMannKendall` is a non-parametric Mann-Kendall trend analysis package implemented in pure Python, which brings together almost all types of Mann-Kendall tests, which might help researchers to check Mann-Kendall trends in Python.

# References
