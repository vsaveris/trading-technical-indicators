"""
Unit tests for the OHLCV data container.
"""

import math
import unittest
from datetime import datetime
from statistics import mean, stdev

from tti.ml.data.ohlcv import OHLCV


class TestOHLCV(unittest.TestCase):
    def test_computed_fields_when_inputs_available(self):
        volume_window = list(range(1000, 1020))  # 20 values, stdev > 0
        bar = OHLCV(
            date=datetime(2024, 1, 2),
            open=10.0,
            high=12.0,
            low=9.0,
            adjusted_close=11.0,
            volume=1000.0,
            prev_adj_close=10.0,
            prev_adj_close_5=9.0,
            prev_adj_close_10=8.0,
            prev_volume=900.0,
            volume_window_20=volume_window,
        )

        self.assertAlmostEqual(bar.ret_1d, math.log(11.0 / 10.0))
        self.assertAlmostEqual(bar.ret_5d, math.log(11.0 / 9.0))
        self.assertAlmostEqual(bar.ret_10d, math.log(11.0 / 8.0))
        self.assertAlmostEqual(bar.price_range, (12.0 - 9.0) / 11.0)
        self.assertAlmostEqual(bar.close_pos, (11.0 - 9.0) / (12.0 - 9.0 + bar.eps))
        self.assertAlmostEqual(bar.vol_chg, (1000.0 / 900.0) - 1.0)

        expected_mu = mean(volume_window)
        expected_sigma = stdev(volume_window)
        self.assertAlmostEqual(bar.vol_zscore_20, (1000.0 - expected_mu) / expected_sigma)

    def test_missing_reference_values_return_none(self):
        bar = OHLCV(
            date=datetime(2024, 1, 2),
            open=10.0,
            high=12.0,
            low=9.0,
            adjusted_close=11.0,
            volume=1000.0,
        )

        self.assertIsNone(bar.ret_1d)
        self.assertIsNone(bar.ret_5d)
        self.assertIsNone(bar.ret_10d)
        self.assertIsNotNone(bar.price_range)
        self.assertIsNotNone(bar.close_pos)
        self.assertIsNone(bar.vol_chg)
        self.assertIsNone(bar.vol_zscore_20)


if __name__ == "__main__":
    unittest.main()
