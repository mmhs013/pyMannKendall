import os
import pytest
import pandas as pd
import pymannkendall as mk

@pytest.fixture
def rainfalldata():
    data = pd.read_csv(os.path.join(os.path.dirname(__file__),"data/Monthly Rainfall.csv"))
    return data
    
@pytest.fixture
def wqdata():
    data = pd.read_csv(os.path.join(os.path.dirname(__file__),"data/Water Quality.csv"))
    return data

def test_original_test(rainfalldata):
    result = mk.original_test(rainfalldata.iloc[:,2])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.37591058740506833
    assert result.z == -0.8854562842589916
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 4889800.333333333
    assert result.slope == -0.0064516129032258064
    
def test_hamed_rao_modification_test(rainfalldata):
    result = mk.hamed_rao_modification_test(rainfalldata.iloc[:,2])
    
    assert result.trend == 'decreasing'
    assert result.h == True
    assert result.p == 0.00011372459883540742
    assert result.z == -3.859273515045842
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 257403.38678462413
    assert result.slope == -0.0064516129032258064
    
def test_hamed_rao_modification_test_lag3(rainfalldata):
    result = mk.hamed_rao_modification_test(rainfalldata.iloc[:,2], lag=3)
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.603684460662274
    assert result.z == -0.5191093899188985
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 14226812.425138814
    assert result.slope == -0.0064516129032258064

def test_yue_wang_modification_test(rainfalldata):
    result = mk.yue_wang_modification_test(rainfalldata.iloc[:,2])
    
    assert result.trend == 'decreasing'
    assert result.h == True
    assert round(result.p, 13) == round(0.008344656549921448, 13)
    assert round(result.z, 12) == round(-2.6377968071103193, 12)
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert round(result.var_s, 6) == round(550988.7079774942, 6)
    assert result.slope == -0.0064516129032258064
    
def test_yue_wang_modification_test_lag1(rainfalldata):
    result = mk.yue_wang_modification_test(rainfalldata.iloc[:,2], lag=1)
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.5433110592605916
    assert result.z == -0.6078136738097195
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 10377301.691383107
    assert result.slope == -0.0064516129032258064
    
def test_pre_whitening_modification_test(rainfalldata):
    result = mk.pre_whitening_modification_test(rainfalldata.iloc[:,2])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.9212742990272651
    assert result.z == -0.09882867695903437
    assert result.Tau == -0.003545066045066045
    assert result.s == -219.0
    assert result.var_s == 4865719.0
    assert round(result.slope, 16) == round(-0.0005373555273865899, 16)
    
def test_trend_free_pre_whitening_modification_test(rainfalldata):
    result = mk.trend_free_pre_whitening_modification_test(rainfalldata.iloc[:,2])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.7741578265217384
    assert result.z == -0.2869405688895601
    assert result.Tau == -0.010262885262885263
    assert result.s == -634.0
    assert result.var_s == 4866576.0
    assert result.slope == -0.004174019670423232
    
def test_seasonal_test(rainfalldata):
    result = mk.seasonal_test(rainfalldata.iloc[:,2], period=12)
    
    assert result.trend == 'decreasing'
    assert result.h == True
    assert result.p == 0.03263834596177739
    assert result.z == -2.136504114534638
    assert result.Tau == -0.0794979079497908
    assert result.s == -399.0
    assert result.var_s == 34702.333333333336
    assert result.slope == -0.16666666666666666
    
def test_regional_test(rainfalldata):
    result = mk.regional_test(rainfalldata.iloc[:,2:])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.06443501180664057
    assert result.z == -1.8491579278636574
    assert result.Tau == -0.02672619796252044
    assert result.s == -10200.0
    assert result.var_s == 30420557.999999996
    assert result.slope == -0.010810810810810811
    
def test_correlated_multivariate_test(rainfalldata):
    result = mk.correlated_multivariate_test(rainfalldata.iloc[:,2:])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.3579989565502104
    assert result.z == -0.9191847304041887
    assert result.Tau == -0.0312970635204792
    assert result.s == -11014.0
    assert result.var_s == 143576890.0
    assert result.slope == -0.010810810810810811
    
def test_correlated_seasonal_test(rainfalldata):
    result = mk.correlated_seasonal_test(rainfalldata.iloc[:,2], period=12)
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.06032641537423844
    assert result.z == -1.878400366918792
    assert result.Tau == -0.10054347826086957
    assert result.s == -333.0
    assert result.var_s == 31427.666666666664
    assert result.slope == -0.16666666666666666
    
def test_partial_test(wqdata):
    result = mk.partial_test(wqdata.iloc[:,2:])
    
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.06670496348739152
    assert result.z == -1.8336567432191642
    assert result.Tau == -0.07552758237689744
    assert result.s == -282.53012319329804
    assert result.var_s == 23740.695506142725
    assert result.slope == -0.6382978723404256