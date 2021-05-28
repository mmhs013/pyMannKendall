# In this unit test file, we check all functions with randomly generated No trendy, trendy, arbitrary data. Those results are compared with R package - modifiedmk, fume, rkt, trend.

import os
import pytest
import numpy as np
import pymannkendall as mk

@pytest.fixture
def NoTrendData():
    # Generate 360 random value with the same number
    NoTrendData = np.ones(360)*np.random.randint(10)
    return NoTrendData

@pytest.fixture
def NoTrend2dData():
    # Generate 2 dimensional 360 random value with same number
    NoTrend2dData = np.ones((360,2))*np.random.randint(10)
    return NoTrend2dData
    
@pytest.fixture
def TrendData():
    # Generate random 360 trendy data with approx. slope 1 
    TrendData = np.arange(360).astype(np.float) + np.random.rand(360)/10**13
    return TrendData

@pytest.fixture
def arbitrary_1d_data():
    # Generate arbitrary 360 data
    arbitrary_1d_data = np.array([ 32.,  20.,  25., 189., 240., 193., 379., 278., 301.,   0.,   0.,
        82.,   0.,   4.,  np.nan,  np.nan, 121., 234., 360., 262., 120.,  30.,
        11.,   1.,   7.,   3.,  31.,  31., 355., 102., 248., 274., 308.,
        np.nan,   5.,  26.,  11.,  16.,   6.,  48., 388., 539., 431., 272.,
       404., 186.,   0.,   2.,   0.,   4.,   1.,  54., 272., 459., 235.,
       164., 365., 135.,   2.,  np.nan,  np.nan,   4.,   0., 128., 210., 163.,
       446., 225., 462., 467.,  19.,  13.,   0.,   3.,  17., 132., 178.,
       338., 525., 623., 145.,  31.,  19.,   3.,   0.,  29.,  25.,  87.,
       259., 756., 486., 180., 292.,  43.,  92.,   1.,   0.,  16.,   2.,
         0., 130., 253., 594., 111., 273.,  30.,   0.,   4.,   0.,  27.,
        24.,  41., 292., 378., 499., 265., 320., 227.,   4.,   0.,   4.,
        14.,   8.,  48., 416., 240., 404., 207., 733., 105.,   0., 112.,
         0.,  14.,   0.,  30., 140., 202., 289., 159., 424., 106.,   3.,
         0.,  65.,   3.,  14.,  58., 268., 466., 432., 266., 240.,  95.,
         1.,   0.,  10.,  26.,   4., 114.,  94., 289., 173., 208., 263.,
       156.,   5.,   0.,  16.,  16.,  14.,   0., 111., 475., 534., 432.,
       471., 117.,  70.,   1.,   3.,  28.,   7., 401., 184., 283., 338.,
       171., 335., 176.,   0.,   0.,  10.,  11.,   9., 140., 102., 208.,
       298., 245., 220.,  29.,   2.,  27.,  10.,  13.,  26.,  84., 143.,
       367., 749., 563., 283., 353.,  10.,   0.,   0.,   0.,   0.,   9.,
       246., 265., 343., 429., 168., 133.,  17.,   0.,  18.,  35.,  76.,
       158., 272., 250., 190., 289., 466.,  84.,   0.,   0.,   0.,   0.,
         0.,  22., 217., 299., 185., 115., 344., 203.,   8.,  np.nan,  np.nan,
         0.,   5., 284., 123., 254., 476., 496., 326.,  27.,  20.,   0.,
         4.,  53.,  72., 113., 214., 364., 219., 220., 156., 264.,   0.,
        13.,   0.,   0.,  45.,  90., 137., 638., 529., 261., 206., 251.,
         0.,   0.,   5.,   9.,  58.,  72., 138., 130., 471., 328., 356.,
       523.,   0.,   1.,   0.,   0.,  12., 143., 193., 184., 192., 138.,
       174.,  69.,   1.,   0.,   0.,  18.,  25.,  28.,  92., 732., 320.,
       256., 302., 131.,  15.,   0.,  27.,   0.,  22.,  20., 213., 393.,
       474., 374., 109., 159.,   0.,   0.,   0.,   3.,   3.,  49., 205.,
       128., 194., 570., 169.,  89.,   0.,   0.,   0.,   0.,   0.,  26.,
       185., 286.,  92., 225., 244., 190.,   3.,  20.])
    return arbitrary_1d_data

@pytest.fixture
def arbitrary_2d_data():
    # Generate arbitrary 80, 2 dimensional data
    arbitrary_2d_data = np.array([[ 490.,  458.], [ 540.,  469.], [ 220., 4630.], [ 390.,  321.], [ 450.,  541.],
       [ 230., 1640.], [ 360., 1060.], [ 460.,  264.], [ 430.,  665.], [ 430.,  680.],
       [ 620.,  650.], [ 460., np.nan], [ 450.,  380.], [ 580.,  325.], [ 350., 1020.],
       [ 440.,  460.], [ 530.,  583.], [ 380.,  777.], [ 440., 1230.], [ 430.,  565.],
       [ 680.,  533.], [ 250., 4930.], [np.nan, 3810.], [ 450.,  469.], [ 500.,  473.],
       [ 510.,  593.], [ 490.,  500.], [ 700.,  266.], [ 420.,  495.], [ 710.,  245.],
       [ 430.,  736.], [ 410.,  508.], [ 700.,  578.], [ 260., 4590.], [ 260., 4670.],
       [ 500.,  503.], [ 450.,  469.], [ 500.,  314.], [ 620.,  432.], [ 670.,  279.],
       [np.nan,  542.], [ 470.,  499.], [ 370.,  741.], [ 410.,  569.], [ 540.,  360.],
       [ 550.,  513.], [ 220., 3910.], [ 460.,  364.], [ 390.,  472.], [ 550.,  245.],
       [ 320., np.nan], [ 570.,  224.], [ 480.,  342.], [ 520.,  732.], [ 620.,  240.],
       [ 520.,  472.], [ 430.,  679.], [ 400., 1080.], [ 430.,  920.], [ 490.,  488.],
       [ 560., np.nan], [ 370.,  595.], [ 460.,  295.], [ 390.,  542.], [ 330., 1500.],
       [ 350., 1080.], [ 480.,  334.], [ 390.,  423.], [ 500.,  216.], [ 410.,  366.],
       [ 470.,  750.], [ 280., 1260.], [ 510.,  223.], [np.nan,  462.], [ 310., 7640.],
       [ 230., 2340.], [ 470.,  239.], [ 330., 1400.], [ 320., 3070.], [ 500.,  244.]])
    return arbitrary_2d_data

def test_sens_slope(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.sens_slope(NoTrendData)
    assert NoTrendRes.slope == 0.0
    
    # check with trendy data
    TrendRes = mk.sens_slope(TrendData)
    assert TrendRes.slope == 1.0
    assert round(TrendRes.intercept) == 0.0
    
    result = mk.sens_slope(arbitrary_1d_data)
    assert result.slope == -0.006369426751592357
    assert result.intercept == 96.15286624203821
    
def test_seasonal_sens_slope(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.seasonal_sens_slope(NoTrendData)
    assert NoTrendRes.slope == 0.0
    
    # check with trendy data
    TrendRes = mk.seasonal_sens_slope(TrendData)
    assert TrendRes.slope == 12.0
    assert round(TrendRes.intercept) == 0.0
    
    result = mk.seasonal_sens_slope(arbitrary_1d_data)
    assert result.slope == -0.08695652173913043
    assert result.intercept == 96.31159420289855

def test_original_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.original_test(NoTrendData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    assert NoTrendRes.var_s == 0.0
    
    # check with trendy data
    TrendRes = mk.original_test(TrendData)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 64620.0
    
    # check with arbitrary data
    result = mk.original_test(arbitrary_1d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.37591058740506833
    assert result.z == -0.8854562842589916
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 4889800.333333333
    
def test_hamed_rao_modification_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.hamed_rao_modification_test(NoTrendData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.hamed_rao_modification_test(TrendData)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 64620.0
    
    # check with arbitrary data
    result = mk.hamed_rao_modification_test(arbitrary_1d_data)
    assert result.trend == 'decreasing'
    assert result.h == True
    assert result.p == 0.00012203829241275166
    assert result.z == -3.8419950613710894
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 259723.81316716125
    
def test_hamed_rao_modification_test_lag3(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.hamed_rao_modification_test(NoTrendData, lag=3)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.hamed_rao_modification_test(TrendData, lag=3)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 64620.0
    
    # check with arbitrary data
    result = mk.hamed_rao_modification_test(arbitrary_1d_data, lag=3)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.6037112685123898
    assert result.z == -0.5190709455046154
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    assert result.var_s == 14228919.889368296

def test_yue_wang_modification_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.yue_wang_modification_test(NoTrendData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.yue_wang_modification_test(TrendData)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 64620.0
    
    # check with arbitrary data
    result = mk.yue_wang_modification_test(arbitrary_1d_data)
    assert result.trend == 'decreasing'
    assert result.h == True
    np.testing.assert_allclose(result.p, 0.008401398144858296)
    np.testing.assert_allclose(result.z, -2.6354977553857504)
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    np.testing.assert_allclose(result.var_s, 551950.4269211816)
    
def test_yue_wang_modification_test_lag1(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.yue_wang_modification_test(NoTrendData, lag=1)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.yue_wang_modification_test(TrendData, lag=1)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 64620.0
    
    # check with arbitrary data
    result = mk.yue_wang_modification_test(arbitrary_1d_data, lag=1)
    assert result.trend == 'no trend'
    assert result.h == False
    np.testing.assert_allclose(result.p, 0.5433112864060043)
    np.testing.assert_allclose(result.z, -0.6078133313683783)
    assert result.Tau == -0.03153167653875869
    assert result.s == -1959.0
    np.testing.assert_allclose(result.var_s, 10377313.384506395)
    
def test_pre_whitening_modification_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.pre_whitening_modification_test(NoTrendData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    
    # check with trendy data
    TrendRes = mk.pre_whitening_modification_test(TrendData)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    
    # check with arbitrary data
    result = mk.pre_whitening_modification_test(arbitrary_1d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.9212742990272651
    assert result.z == -0.09882867695903437
    assert result.Tau == -0.003545066045066045
    assert result.s == -219.0
    assert result.var_s == 4865719.0
    
def test_trend_free_pre_whitening_modification_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.trend_free_pre_whitening_modification_test(NoTrendData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    
    # check with trendy data
    TrendRes = mk.trend_free_pre_whitening_modification_test(TrendData)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    
    # check with arbitrary data
    result = mk.trend_free_pre_whitening_modification_test(arbitrary_1d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.7755465706913385
    assert result.z == -0.28512735834365455
    assert result.Tau == -0.010198135198135198
    assert result.s == -630.0
    assert result.var_s == 4866576.0
    
def test_seasonal_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.seasonal_test(NoTrendData, period=12)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.seasonal_test(TrendData, period=12)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert TrendRes.p == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 5220.0
    
    # check with arbitrary data
    result = mk.seasonal_test(arbitrary_1d_data, period=12)
    assert result.trend == 'decreasing'
    assert result.h == True
    assert result.p == 0.03263834596177739
    assert result.z == -2.136504114534638
    assert result.Tau == -0.0794979079497908
    assert result.s == -399.0
    assert result.var_s == 34702.333333333336
    
def test_regional_test(NoTrend2dData,arbitrary_2d_data):
    # check with no trend data
    NoTrendRes = mk.regional_test(NoTrend2dData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    assert NoTrendRes.var_s == 0.0
    assert NoTrendRes.slope == 0.0
    
    # check with arbitrary data
    result = mk.regional_test(arbitrary_2d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.2613018311185482
    assert result.z == -1.1233194854000186
    assert result.Tau == -0.06185919343814081
    assert result.s == -362.0
    assert result.var_s == 103278.0
    assert result.slope == -0.680446465481604
    
def test_correlated_multivariate_test(NoTrend2dData,arbitrary_2d_data):
    # check with no trend data
    NoTrendRes = mk.correlated_multivariate_test(NoTrend2dData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    assert NoTrendRes.var_s == 0.0
    assert NoTrendRes.slope == 0.0
    
    # check with arbitrary data
    result = mk.correlated_multivariate_test(arbitrary_2d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.05777683185903615
    assert result.z == -1.8973873659119118
    assert result.Tau == -0.05868196964087375
    assert result.s == -317.0
    assert result.var_s == 27913.000000000007
    assert result.slope == -0.680446465481604
    
def test_correlated_seasonal_test(NoTrendData, TrendData, arbitrary_1d_data):
    # check with no trend data
    NoTrendRes = mk.correlated_seasonal_test(NoTrendData, period=12)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    
    # check with trendy data
    TrendRes = mk.correlated_seasonal_test(TrendData, period=12)
    assert TrendRes.trend == 'increasing'
    assert TrendRes.h == True
    assert round(TrendRes.p) == 0.0
    assert TrendRes.Tau == 1.0
    assert TrendRes.s == 5220.0
    
    # check with arbitrary data
    result = mk.correlated_seasonal_test(arbitrary_1d_data, period=12)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.06032641537423844
    assert result.z == -1.878400366918792
    assert result.Tau == -0.10054347826086957
    assert result.s == -333.0
    assert result.var_s == 31427.666666666664
    
def test_partial_test(NoTrend2dData,arbitrary_2d_data):
    # check with no trend data
    NoTrendRes = mk.partial_test(NoTrend2dData)
    assert NoTrendRes.trend == 'no trend'
    assert NoTrendRes.h == False
    assert NoTrendRes.p == 1.0
    assert NoTrendRes.z == 0
    assert NoTrendRes.Tau == 0.0
    assert NoTrendRes.s == 0.0
    assert NoTrendRes.var_s == 5205500.0
    
    # check with arbitrary data
    result = mk.partial_test(arbitrary_2d_data)
    assert result.trend == 'no trend'
    assert result.h == False
    assert result.p == 0.06670496348739152
    assert result.z == -1.8336567432191642
    assert result.Tau == -0.07552758237689744
    assert result.s == -282.53012319329804
    assert result.var_s == 23740.695506142725
    assert result.slope == -0.5634920634920635
    assert result.intercept == 471.9761904761905