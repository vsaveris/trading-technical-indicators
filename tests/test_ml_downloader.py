"""
Trading-Technical-Indicators (tti) python library

File name: test_ml_downloader.py
    tti.ml.data.downloader package unit tests.
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from tti.ml.data.downloaders._downloader import (
    DailyPriceDownloader,
    _nasdaq_holidays,
)


class DummyDownloader(DailyPriceDownloader):
    source = "Dummy"

    def _fetch(
        self, asset: str, start_date: pd.Timestamp | None, end_date: pd.Timestamp | None
    ) -> pd.DataFrame:
        # Generate simple business-day OHLCV rows between start and end (inclusive).
        start = start_date or pd.Timestamp("2020-01-01")
        end = end_date or start
        dates = pd.date_range(start=start, end=end, freq="B")
        return pd.DataFrame(
            {
                "date": dates,
                "open": range(len(dates)),
                "high": range(len(dates)),
                "low": range(len(dates)),
                "close": range(len(dates)),
                "adj_close": range(len(dates)),
                "volume": range(len(dates)),
            }
        )


def test_validate_data_requires_date_column():
    dl = DummyDownloader()
    with pytest.raises(ValueError):
        dl._validate_data(pd.DataFrame({"foo": [1, 2, 3]}))


def test_download_persists_files(tmp_path: Path):
    dl = DummyDownloader()
    meta = dl.download("TEST", data_dir=tmp_path, start_date="2020-01-01", end_date="2020-01-03")

    expected_csv = tmp_path / meta["data_file"]
    expected_meta = expected_csv.with_suffix(".metadata.json")
    assert expected_csv.exists()
    assert expected_meta.exists()

    with expected_meta.open() as fh:
        stored = json.load(fh)

    assert stored["asset"] == "TEST"
    assert stored["source"] == "Dummy"
    assert stored["rows"] == 3
    assert stored["status"] == "OK"
    assert stored["missing_dates"] == []

    df = pd.read_csv(expected_csv)
    assert set(df.columns) == {"date", "open", "high", "low", "close", "volume", "adj_close"}


def test_update_adds_forward_segment(tmp_path: Path):
    dl = DummyDownloader()
    dl.download("TEST", data_dir=tmp_path, start_date="2020-01-01", end_date="2020-01-03")
    meta = dl.update("TEST", data_dir=tmp_path, end_date="2020-01-07")

    updated_path = tmp_path / meta["data_file"]
    assert updated_path.exists()
    assert meta["rows"] == 5  # Jan 1,2,3,6,7 (business days)
    assert meta["start_date"] == "2020-01-01"
    assert meta["end_date"] == "2020-01-07"

    df = pd.read_csv(updated_path, parse_dates=["date"])
    assert df["date"].min().date().isoformat() == "2020-01-01"
    assert df["date"].max().date().isoformat() == "2020-01-07"


def test_nasdaq_holidays_returns_empty_without_calendar(monkeypatch):
    # Ensure mcal import is treated as missing
    from tti.ml.data.downloaders import _downloader as dl_module

    monkeypatch.setattr(dl_module, "mcal", None, raising=True)
    holidays = _nasdaq_holidays(pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-31"))
    assert holidays == []
