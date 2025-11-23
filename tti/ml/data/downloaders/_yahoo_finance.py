"""
Trading-Technical-Indicators (tti) python library

File name: _yahoo_finance.py
    Yahoo Finance online source, downloader implementation.
"""

from __future__ import annotations
from typing import Optional

import pandas as pd
import yfinance as yf
from pandas.tseries.offsets import BDay

from ._downloader import DailyPriceDownloader


class YahooFinanceDailyDownloader(DailyPriceDownloader):
    source = "Yahoo Finance"

    def _fetch(
        self, asset: str, start_date: Optional[pd.Timestamp], end_date: Optional[pd.Timestamp]
    ) -> pd.DataFrame:
        # yfinance treats end as exclusive; push one business day forward for inclusive range
        adjusted_end = (end_date + BDay(1)) if end_date is not None else None

        # When no start_date is provided, request full history (period="max") so we don't get only 1 month.
        download_kwargs = {
            "end": adjusted_end.to_pydatetime() if adjusted_end is not None else None,
            "progress": False,
            "auto_adjust": False,
        }
        if start_date is None:
            download_kwargs["period"] = "max"
        else:
            download_kwargs["start"] = start_date.to_pydatetime()

        history = yf.download(asset, **download_kwargs)

        if history.empty:
            raise ValueError(
                f"No data returned from Yahoo Finance for {asset}. "
                "Verify the ticker symbol and availability."
            )

        # Flatten possible multi-index columns (e.g., when multiple tickers are passed)
        history.columns = [c[0] if isinstance(c, tuple) else c for c in history.columns]

        history = history.reset_index()
        if "Date" not in history.columns and "index" in history.columns:
            history = history.rename(columns={"index": "Date"})
        if "Date" not in history.columns:
            history.insert(0, "Date", history.index)

        history = history.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )

        return history[["date", "open", "high", "low", "close", "adj_close", "volume"]]
