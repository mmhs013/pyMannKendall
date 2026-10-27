import numpy as np
import pytest
import pymannkendall as mk


@pytest.mark.parametrize('container', [list, tuple])
@pytest.mark.parametrize('values, intercept', [
    ([1, 10, 2, 11, 3, 12], 5.25),
    ([1, 10, 2, 11, 3], 2.0),
    ([1, 10, np.nan, 11, 3, 12, 4], 5.25),
])
def test_seasonal_slope_accepts_sequences(container, values, intercept):
    result = mk.seasonal_sens_slope(container(values), period=2)

    assert result.slope == 1.0
    assert result.intercept == intercept


def test_seasonal_slope_accepts_series():
    pd = pytest.importorskip('pandas')
    values = pd.Series([1, 10, np.nan, 11, 3, 12, 4], index=range(10, 17))

    result = mk.seasonal_sens_slope(values, period=2)

    assert result.slope == 1.0
    assert result.intercept == 5.25


def test_seasonal_slope_preserves_masked_array_intercept():
    values = np.ma.array([1., 10., 2., 11., 3., 12.],
                         mask=[False, False, False, True, False, False])

    result = mk.seasonal_sens_slope(values, period=2)

    assert result.slope == 1.0
    assert result.intercept == 1.75
