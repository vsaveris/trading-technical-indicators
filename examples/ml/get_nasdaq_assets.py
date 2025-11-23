"""
Trading-Technical-Indicators (tti) python library

File name: get_nasdaq_assets.py
    Get all assets from NASDAQ (exclude test assets), based on the passed filtering criteria.

Use as:
    python get_nasdaq_assets.py
"""

import pandas as pd

from tti.ml.data import get_available_assets, MarketCategory, FinancialStatus

if __name__ == "__main__":
    data = get_available_assets(
        nasdaq_listed_url="https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt",
        market_categories=[MarketCategory.GLOBAL_SELECT],
        financial_statuses=[FinancialStatus.NORMAL],
        ignore_etfs=True,
        ignore_next_shares=True,
    )

    with pd.option_context("display.max_columns", None, "display.expand_frame_repr", False):
        print(data.head(5).to_string(index=False))
