import numpy as np
import pymannkendall as mk
import pytest


@pytest.mark.parametrize("alpha, expected", [(0.01, False), (0.05, True), (0.10, True)])
@pytest.mark.parametrize("flatten", [False, True])
@pytest.mark.parametrize("direction", [1, -1])
def test_correlated_seasonal_alpha(alpha, expected, flatten, direction):
    data = direction * np.column_stack([np.arange(1, 6), 10 * np.arange(1, 6)])
    result = mk.correlated_seasonal_test(
        data.ravel() if flatten else data, period=2, alpha=alpha
    )

    assert result.p == pytest.approx(0.014305878435429742)
    assert bool(result.h) is expected
    assert result.trend == (
        ("increasing" if direction == 1 else "decreasing") if expected else "no trend"
    )
    assert result.z == pytest.approx(direction * np.sqrt(6))
    assert result.s == direction * 20
    assert result.var_s == pytest.approx(200 / 3)
