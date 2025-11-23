"""
Trading-Technical-Indicators (tti) python library

File name: test_ml_nasdaq.py
    tti.ml.data, _nasdaq module unit tests.
"""

import textwrap

import pandas as pd

from tti.ml.data import get_available_assets, MarketCategory, FinancialStatus


def test_get_available_assets_filters_symbols(monkeypatch):
    sample_text = textwrap.dedent(
        """\
        Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
        AAPL|Apple Inc.|Q|N|N|100|N|N
        TESTETF|Test ETF|Q|N|N|100|Y|N
        TESTISSUE|Test Issue|Q|Y|N|100|N|N
        File Creation Time: 20250101|||||||
        """
    )

    class DummyResp:
        def __init__(self, text: str):
            self.text = text

        def raise_for_status(self):
            return None

    monkeypatch.setattr(
        "tti.ml.data._nasdaq.requests.get",
        lambda url, timeout=10: DummyResp(sample_text),
    )

    df = get_available_assets(
        nasdaq_listed_url="mock://nasdaq",
        market_categories=[MarketCategory.GLOBAL_SELECT],
        financial_statuses=[FinancialStatus.NORMAL],
        ignore_etfs=True,
        ignore_next_shares=True,
    )

    assert isinstance(df, pd.DataFrame)
    assert list(df["Symbol"]) == ["AAPL"]
