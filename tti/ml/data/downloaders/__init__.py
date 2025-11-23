"""
Data downloaders for daily OHLCV market data.

Provides a common abstract interface and concrete implementations for downloading 1-day granularity data from online
sources.
"""

from ._yahoo_finance import YahooFinanceDailyDownloader

__all__ = [YahooFinanceDailyDownloader]
