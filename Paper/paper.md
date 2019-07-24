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

Trend analysis is one of the important measurements in studying time series data. Both parametric and non-parametric tests are commonly used in trend analysis. Parametric test requires data to be independent and normally distributed. On the other hand, non-parametric trend tests require only that the data be independent and can tolerate outliers in the data [@hamed1998modified]. However, Parametric tests are more powerful than nonparametric ones.

The Mann–Kendall trend test [@mann1945nonparametric; @kendall1975rank] is one of the widely used non-parametric tests to detect significant trends in time series. However, the original Mann-Kendall test didn't consider serial correlation or seasonality effects [@bari2016analysis; @hirsch1982techniques]. But, in many real situations, the observed data are autocorrelated and this autocorrelation will result in misinterpretation of trend tests results [@hamed1998modified, @cox1955some]. Contrariwise, water quality, hydrologic, as well as climatic and other natural time series also have seasonality. To overcome those limitations of original Mann-Kendall test, various modified Mann-Kendall test has developed.

Again, Python is one of the widely used tools for data analysis. A large number of data analysis and research tools are also developed using python. But, till now, there is no Mann-Kendall trend relation python package available. ``pyMannKendall`` package is going to fill up this gap.

``pyMannKendall`` is written in pure python and use vectorization approach to increase its performance. Currently, this package has 11 Mann-Kendall Tests and 2 sen’s slope estimator function. Brief description of functions are below:

1.	**Original Mann-Kendall test (*original_test*):** Original Mann-Kendall test [@mann1945nonparametric; @kendall1975rank] is a nonparametric test, which does not consider serial correlation or seasonal effects.

2.	**Hamed and Rao Modified MK Test (*hamed_rao_modification_test*):** This modified MK test proposed by Hamed and Rao [@hamed1998modified] to address serial autocorrelation issues. They suggested a variance correction approach to improve trend analysis. User can consider first n significant lag by insert lag number in this function. By default, it considered all significant lags.

3.	**Yue and Wang Modified MK Test (*yue_wang_modification_test*):** This is also a variance correction method for considered serial autocorrelation proposed by Yue, S., & Wang, C. Y. [@yue2004mann]. User can also set their desired significant n lags for the calculation.

4.	**Modified MK test using Pre-Whitening method (*pre_whitening_modification_test*):** This test suggested by Yue and Wang [@yue2002applicability] to using Pre-Whitening the time series before the application of trend test.

5.	**Modified MK test using Trend free Pre-Whitening method (*trend_free_pre_whitening_modification_test*):** This test also proposed by Yue and Wang [@yue2002influence] to remove trend component and then Pre-Whitening the time series before application of trend test.

6.	**Multivariate MK Test (*multivariate_test*):** This is an MK test for multiple parameters proposed by Hirsch [@hirsch1982techniques]. He used this method for seasonal mk test, where he considered every month as a parameter.

7.	**Seasonal MK Test (*seasonal_test*):** For seasonal time series data, Hirsch, R.M., Slack, J.R. and Smith, R.A. [@hirsch1982techniques] proposed this test to calculate the seasonal trend.

8.	**Regional MK Test (*regional_test*):** Based on Hirsch [@hirsch1982techniques] proposed seasonal mk test, Helsel, D.R. and Frans, L.M. [@helsel2006regional] suggest regional mk test to calculate the overall trend in a regional scale.

9.	**Correlated Multivariate MK Test (*correlated_multivariate_test*):** This multivariate mk test proposed by Hipel [@hipel1994time] where the parameters are correlated.

10.	**Correlated Seasonal MK Test (*correlated_seasonal_test*):** This method proposed by Hipel [@hipel1994time] used, when time series significantly correlated with the preceding one or more months/seasons.

11.	**Partial MK Test (*partial_test*):** In a real event, many factors are affecting the main studied response parameter, which can bias the trend results. To overcome this problem, Libiseller [@libiseller2002performance] proposed this partial mk test. It required two parameters as input, where, one is response parameter and other is an independent parameter.

12.	**Theil-sen's Slope Estimator (*sens_slope*):** This method proposed by Theil [@theil1950rank] and Sen [@sen1968estimates] to estimate the magnitude of the monotonic trend.

13.	**Seasonal sen's Slope Estimator (*seasonal_sens_slope*):** This method proposed by Hipel [@hipel1994time] to estimate the magnitude of the monotonic trend, when data has seasonal effects.


`pyMannKendall` is a pure Python implemented non-parametric Mann-Kendall trend analysis package, which bring together almost all types of Mann-Kendall Test, which might help researchers to check the Mann-Kendall trend in python.

# References
