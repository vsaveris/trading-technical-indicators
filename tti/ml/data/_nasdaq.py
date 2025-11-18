"""
Trading-Technical-Indicators (tti) python library

File name: _nasdaq.py
    Implements a function for NASDAQ assets retrieval.
"""

from typing import List
from enum import Enum
from io import StringIO
import requests

import pandas as pd

from ...utils.exceptions import NasdaqAssetsRetrievalError


class MarketCategory(Enum):
    """
    A letter indicating which NASDAQ "tier" the company trades on:

    Code	Meaning	                        Description
    Q	    NASDAQ Global Select Market	    Highest listing standards
    G	    NASDAQ Global Market	        Middle tier
    S	    NASDAQ Capital Market	        For smaller/younger companies
    """

    GLOBAL_SELECT = "Q"
    GLOBAL = "G"
    CAPITAL = "S"


class FinancialStatus(Enum):
    """
    Indicates whether the company has financial compliance issues such as bankruptcy:
    Code	Meaning
    N	    Normal
    D	    Deficient (fails NASDAQ listing standards)
    E	    Delinquent (missed filings/reporting)
    Q	    Bankrupt
    G	    Deficient and Bankrupt
    H	    Deficient and Delinquent
    J	    Delinquent and Bankrupt
    K	    Deficient, Delinquent, and Bankrupt
    """

    NORMAL = "N"
    DEFICIENT = "D"
    DELINQUENT = "E"
    BANKRUPT = "Q"
    DEFICIENT_AND_BANKRUPT = "G"
    DEFICIENT_AND_DELINQUENT = "H"
    DELINQUENT_AND_BANKRUPT = "J"
    DEFICIENT_AND_DELINQUENT_AND_BANKRUPT = "K"


def get_available_assets(
    nasdaq_listed_url: str,
    market_categories: List[MarketCategory],
    financial_statuses: List[FinancialStatus],
    ignore_etfs: bool = True,
    ignore_next_shares: bool = True,
) -> pd.DataFrame:
    """
    Retrieve and filter NASDAQ-listed assets from the official NASDAQ symbol directory file, returning the result as a
    pandas DataFrame.

    This function downloads the `nasdaqlisted.txt` dataset from the given URL, parses its metadata fields, applies
    multiple filtering criteria, and returns a cleaned DataFrame containing only the securities that meet the specified
    requirements.

    Parameters
    ----------
    nasdaq_listed_url : str
        URL to the NASDAQ symbol directory file (typically `nasdaqlisted.txt`). The file must contain the standard
        NASDAQ fields: Symbol, SecurityName, MarketCategory, TestIssue, FinancialStatus, RoundLotSize, ETF, NextShares.

    market_categories : List[MarketCategory]
        A set of `MarketCategory` enum values specifying which NASDAQ market tiers to include.

    financial_statuses : List[FinancialStatus]
        A set of `FinancialStatus` enum values indicating which financial compliance categories are acceptable.

    ignore_etfs : bool, optional
        If True (default), ETF-flagged symbols are excluded.
        If False, exchange-traded funds (ETF == 'Y') are included.

    ignore_next_shares : bool, optional
        If True (default), NextShares products (NextShares == 'Y') are excluded. These products are obsolete and
        typically not relevant to most trading universes.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing all NASDAQ-listed securities that satisfy the filtering criteria. Only real (non-test)
        issues are included. The returned DataFrame preserves all parsed NASDAQ directory fields.

    Raises
    ------
    NasdaqAssetsRetrievalError
        If the downloaded file is missing expected columns or cannot be parsed into the expected NASDAQ symbol directory
        structure.

    Notes
    -----
    - Test issues (TestIssue == 'Y') are always removed.
    - No validation of symbol liquidity or active trading status is performed.
    - Caller is responsible for providing a valid download URL.
    """
    required_cols = {
        "Symbol",
        "Security Name",
        "Market Category",
        "Test Issue",
        "Financial Status",
        "Round Lot Size",
        "ETF",
        "NextShares",
    }

    try:
        resp = requests.get(nasdaq_listed_url, timeout=10)
        resp.raise_for_status()

        buffer = StringIO(resp.text)
        df = pd.read_csv(buffer, sep="|", engine="python")

        # Last row is a footer with dataset generation time
        df = df.iloc[:-1].reset_index(drop=True)

        missing_columns = required_cols.difference(df.columns)
        if missing_columns:
            raise ValueError(f"Missing expected NASDAQ columns: {sorted(missing_columns)}")

        # Keep only real trading symbols (exclude test issues)
        df = df[df["Test Issue"] == "N"]

        # Apply filters
        df = df[df["Market Category"].isin([x.value for x in market_categories])]
        df = df[df["Financial Status"].isin([x.value for x in financial_statuses])]
        if ignore_etfs:
            df = df[df["ETF"] == "N"]
        if ignore_next_shares:
            df = df[df["NextShares"] == "N"]

        df = df.reset_index(drop=True)

    except Exception as e:
        raise NasdaqAssetsRetrievalError(
            nasdaq_listed_url,
            market_categories,
            financial_statuses,
            ignore_etfs,
            ignore_next_shares,
            e,
        )

    return df
