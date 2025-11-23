"""
Unit tests for the OHLCV data container.
"""

import math
import unittest
from datetime import datetime

import numpy as np
import pandas as pd

from tti.ml.data.ohlcv import OHLCV


class TestOHLCV(unittest.TestCase):
    def test_computed_fields_when_inputs_available(self):
        # Build 21 bars so rolling windows and shifted returns are defined on the last row.
        rows = 21
        dates = pd.date_range("2024-01-01", periods=rows, freq="D")
        base = np.arange(rows, dtype=float)
        df = pd.DataFrame(
            {
                "date": dates,
                "open": base + 10.0,
                "high": base + 12.0,  # high - low == 3
                "low": base + 9.0,
                "close": base + 11.0,
                "adj_close": base + 11.0,
                "volume": 1000.0 + base,  # simple increasing volume
            }
        ).set_index("date")

        enriched_df = OHLCV(df).df
        bar = enriched_df.iloc[-1]

        # Expected values computed from the source df
        self.assertAlmostEqual(
            bar["log_return_1d"],
            math.log(df["adj_close"].iloc[-1] / df["adj_close"].iloc[-2]),
        )
        self.assertAlmostEqual(
            bar["log_return_5d"],
            math.log(df["adj_close"].iloc[-1] / df["adj_close"].iloc[-6]),
        )

        expected_range_pct = (df["high"].iloc[-1] - df["low"].iloc[-1]) / df["adj_close"].iloc[-1]
        self.assertAlmostEqual(bar["range_pct"], expected_range_pct)

        expected_close_loc = (df["adj_close"].iloc[-1] - df["low"].iloc[-1]) / (
            df["high"].iloc[-1] - df["low"].iloc[-1]
        )
        self.assertAlmostEqual(bar["close_location"], expected_close_loc)

        expected_vol_chg = df["volume"].pct_change().iloc[-1]
        self.assertAlmostEqual(bar["volume_change"], expected_vol_chg)

        window = df["volume"].rolling(20)
        expected_z = (df["volume"].iloc[-1] - window.mean().iloc[-1]) / window.std().iloc[-1]
        self.assertAlmostEqual(bar["zscore_20"], expected_z)

    def test_missing_reference_values_return_nan(self):
        # Single row: shifted and rolling values should be NaN
        df = pd.DataFrame(
            {
                "date": [datetime(2024, 1, 2)],
                "open": [10.0],
                "high": [12.0],
                "low": [9.0],
                "close": [11.0],
                "adj_close": [11.0],
                "volume": [1000.0],
            }
        ).set_index("date")

        bar = OHLCV(df).df.iloc[0]

        self.assertTrue(math.isnan(bar["log_return_1d"]))
        self.assertTrue(math.isnan(bar["log_return_5d"]))
        self.assertIsNotNone(bar["range_pct"])
        self.assertIsNotNone(bar["close_location"])
        self.assertTrue(math.isnan(bar["volume_change"]))
        self.assertTrue(math.isnan(bar["zscore_20"]))


if __name__ == "__main__":
    unittest.main()
