import pandas as pd
import numpy as np


class OHLCV:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

        self.df["log_return_1d"] = self._get_log_return(periods=1)
        self.df["log_return_5d"] = self._get_log_return(periods=5)
        self.df["range_pct"] = self._get_range_as_percentage_of_price()
        self.df["close_location"] = self._get_close_location()
        self.df["volume_change"] = self._get_volume_change()
        self.df["zscore_20"] = self._get_volume_zscore(periods=20)

    def _get_log_return(self, periods: int):
        return np.log(self.df["adj_close"] / self.df["adj_close"].shift(periods))

    def _get_range_as_percentage_of_price(self):
        return (self.df["high"] - self.df["low"]) / self.df["adj_close"]

    def _get_close_location(self):
        return (self.df["adj_close"] - self.df["low"]) / (self.df["high"] - self.df["low"]).replace(
            0, np.nan
        )

    def _get_volume_change(self):
        return self.df["volume"].pct_change()

    def _get_volume_zscore(self, periods: int):
        return (self.df["volume"] - self.df["volume"].rolling(periods).mean()) / self.df[
            "volume"
        ].rolling(periods).std()
