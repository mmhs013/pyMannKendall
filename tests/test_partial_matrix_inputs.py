import numpy as np
import pytest
import pymannkendall as mk


@pytest.mark.parametrize('container', [list, tuple])
@pytest.mark.parametrize('missing', [None, (2, 0), (4, 1)])
def test_partial_slope_keeps_original_time_positions(container, missing):
    data = np.array([[1, 4], [3, 1], [5, 6], [7, 3], [9, 7], [11, 2]],
                    dtype=float)
    if missing is not None:
        data[missing] = np.nan

    result = mk.partial_test(container(data.tolist()))

    assert result.slope == 2.0
    assert result.intercept == 1.0


@pytest.mark.parametrize('container', [list, tuple])
def test_partial_matrix_matches_permutation_reference(container):
    data = [[1, 4], [4, 1], [2, 6], [7, 3], [5, 7], [8, 2]]

    result = mk.partial_test(container(data))

    # All 6! permutations of the paired records give Var(Sx)=85/3 and
    # Cov(Sx, Sy)=-25/3, with observed scores Sx=11 and Sy=1.
    assert result.s == pytest.approx(192 / 17)
    assert result.var_s == pytest.approx(440 / 17)
    assert result.Tau == pytest.approx(11 / 15)
    assert result.p == pytest.approx(0.026419650609668333)
    assert result.slope == 1.4
    assert result.intercept == 1.0


def test_partial_accepts_dataframe():
    pd = pytest.importorskip('pandas')
    data = pd.DataFrame([[1, 4], [4, 1], [2, 6], [7, 3], [5, 7], [8, 2]],
                        columns=['response', 'covariate'], index=range(10, 16))

    result = mk.partial_test(data)

    assert result.slope == 1.4
    assert result.intercept == 1.0
