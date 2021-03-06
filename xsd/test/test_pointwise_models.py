import numpy as np
import pandas as pd

import pytest

from xsd.pointwise_models.utils import LinearTrendTransformer, QuantileMapper


def test_linear_trend_roundtrip():
    # TODO: there is probably a better analytic test here
    n = 100
    trend = 1
    yint = 15

    trendline = trend * np.arange(n) + yint
    noise = np.sin(np.linspace(-10*np.pi, 10*np.pi, n)) * 10
    data = trendline + noise

    ltt = LinearTrendTransformer()

    # remove trend
    d_no_trend = ltt.fit_transform(data)

    # assert detrended data is equal to noise
    np.testing.assert_almost_equal(d_no_trend, noise, decimal=0)
    # assert linear coef is equal to trend
    np.testing.assert_almost_equal(ltt.lr_model_.coef_, trend, decimal=0)
    # assert roundtrip
    np.testing.assert_array_equal(
        ltt.inverse_transform(d_no_trend), data)


def test_quantile_mapper():
    n = 100
    expected = np.sin(np.linspace(-10*np.pi, 10*np.pi, n)) * 10
    with_bias = expected + 2

    mapper = QuantileMapper()
    mapper.fit(expected)
    actual = mapper.transform(with_bias)
    np.testing.assert_almost_equal(
        actual.squeeze(), expected)


@pytest.mark.xfail(reason='Need 3 part QM routine to handle bias removal')
def test_quantile_mapper_detrend():
    n = 100
    trend = 1
    yint = 15

    trendline = trend * np.arange(n) + yint
    base = np.sin(np.linspace(-10*np.pi, 10*np.pi, n)) * 10
    expected = base + trendline
    
    with_bias = expected + 2

    mapper = QuantileMapper(detrend=True)
    mapper.fit(base)
    actual = mapper.transform(with_bias)
    np.testing.assert_almost_equal(
        actual.squeeze(), expected)

