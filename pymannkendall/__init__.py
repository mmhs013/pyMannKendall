from .pymannkendall import sens_slope, seasonal_sens_slope, original_test, hamed_rao_modification_test, yue_wang_modification_test, pre_whitening_modification_test, trend_free_pre_whitening_modification_test, multivariate_test, seasonal_test, regional_test, correlated_multivariate_test, correlated_seasonal_test, partial_test

__all__ = [sens_slope, seasonal_sens_slope, original_test, hamed_rao_modification_test, yue_wang_modification_test, pre_whitening_modification_test, trend_free_pre_whitening_modification_test, multivariate_test, seasonal_test, regional_test, correlated_multivariate_test, correlated_seasonal_test, partial_test]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions