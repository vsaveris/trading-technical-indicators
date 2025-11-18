"""
Trading-Technical-Indicators (tti) python library

File name: _downloader.py
    Implements the downloader API.
"""

from __future__ import annotations
import datetime as dt
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


import pandas_market_calendars as mcal
import pandas as pd
from pandas.tseries.offsets import BDay

DateLike = Optional[Union[str, dt.date, dt.datetime, pd.Timestamp]]


def _normalize_date(value: DateLike) -> Optional[pd.Timestamp]:
    if value is None:
        return None

    return pd.Timestamp(value).normalize()


def _today() -> pd.Timestamp:
    return pd.Timestamp("today").normalize()


def _nasdaq_holidays(start: pd.Timestamp, end: pd.Timestamp) -> List[pd.Timestamp]:
    """
    Retrieve NASDAQ holiday dates between start and end (inclusive) if calendar is available.

    Returns an empty list when `pandas_market_calendars` is not installed.
    """
    if mcal is None:
        return []

    try:
        cal = mcal.get_calendar("NASDAQ")
        trading_days = cal.valid_days(start_date=start, end_date=end, tz=None).tz_localize(None)
        business_days = pd.date_range(start=start, end=end, freq="B")
        holidays = business_days.difference(trading_days)
        return [pd.Timestamp(h).normalize() for h in holidays]
    except Exception:
        # If calendar lookup fails, fall back to no holidays excluded.
        return []


class DailyPriceDownloader(ABC):
    """
    Abstract class for downloading daily OHLCV data to disk with metadata and quality checks.
    """

    def __init__(self):
        pass

    @staticmethod
    def _resolve_data_dir(data_dir: Union[str, Path]) -> Path:
        """
        Resolve the directory where data and metadata files should be written or read from.

        The directory is created if it does not exist.
        """
        target = Path(data_dir)
        target.mkdir(parents=True, exist_ok=True)
        return target

    @property
    @abstractmethod
    def source(self) -> str:
        """Human-friendly name of the data provider."""

    @abstractmethod
    def _fetch(
        self, asset: str, start_date: Optional[pd.Timestamp], end_date: Optional[pd.Timestamp]
    ) -> pd.DataFrame:
        """Return a DataFrame with columns date, open, high, low, close, adj_close, volume."""

    def download(
        self,
        asset: str,
        data_dir: Union[str, Path],
        start_date: Optional[DateLike] = None,
        end_date: Optional[DateLike] = None,
    ) -> Dict:
        """
        Download daily OHLCV data for the given asset and persist it with metadata/validation.

        Parameters
        ----------
        asset : str
            Ticker symbol as understood by the underlying data source.
        data_dir : str | Path
            Target directory for the data/metadata files.
        start_date : DateLike, optional
            Inclusive start date. If None, the oldest available date is used.
        end_date : DateLike, optional
            Inclusive end date. If None, today is used.
        """
        target_dir = self._resolve_data_dir(data_dir)
        start_ts = _normalize_date(start_date)
        end_ts = _normalize_date(end_date) or _today()
        df = self._fetch(asset, start_ts, end_ts)
        metadata = self._persist(asset, df, target_dir)
        self._print_summary(metadata)
        return metadata

    def update(
        self,
        asset: str,
        data_dir: Union[str, Path],
        start_date: Optional[DateLike] = None,
        end_date: Optional[DateLike] = None,
    ) -> Dict:
        """
        Update existing data by downloading only missing date ranges, then re-validating/merging.

        Parameters
        ----------
        asset : str
            Ticker symbol as understood by the underlying data source.
        data_dir : str | Path
            Target directory for the data/metadata files.
        start_date : DateLike, optional
            Desired inclusive start date. If None, uses current data start.
        end_date : DateLike, optional
            Desired inclusive end date. If None, uses today.
        """
        target_dir = self._resolve_data_dir(data_dir)
        end_ts = _normalize_date(end_date) or _today()
        requested_start = _normalize_date(start_date)
        latest_meta_path = self._latest_metadata_path(asset, target_dir)
        if latest_meta_path is None:
            return self.download(
                asset, start_date=requested_start, end_date=end_ts, data_dir=target_dir
            )

        with latest_meta_path.open() as fh:
            existing_meta = json.load(fh)

        data_file = target_dir / existing_meta["data_file"]
        existing_df = pd.read_csv(data_file, parse_dates=["date"])
        existing_df["date"] = existing_df["date"].dt.normalize()

        current_start = pd.Timestamp(existing_meta["start_date"])
        current_end = pd.Timestamp(existing_meta["end_date"])

        target_start = requested_start or current_start
        target_end = end_ts

        segments: List[Tuple[pd.Timestamp, pd.Timestamp]] = []
        if target_start < current_start:
            segments.append((target_start, current_start - BDay(1)))
        if target_end > current_end:
            segments.append((current_end + BDay(1), target_end))

        if not segments:
            metadata = self._persist(asset, existing_df, target_dir)
            self._print_summary(metadata, already_exists=True)
            return metadata

        fetched_segments = []
        for start, end in segments:
            fetched_segments.append(self._fetch(asset, start, end))

        updated_df = pd.concat([existing_df, *fetched_segments], axis=0, ignore_index=True)
        metadata = self._persist(asset, updated_df, target_dir)
        self._print_summary(metadata)
        return metadata

    @staticmethod
    def _validate_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        renamed = df.copy()
        renamed.columns = [col if isinstance(col, str) else str(col) for col in renamed.columns]

        if "date" not in renamed.columns:
            raise ValueError("Downloaded data missing required 'date' column.")

        normalized = renamed.copy()
        normalized["date"] = pd.to_datetime(normalized["date"]).dt.normalize()
        normalized = normalized.drop_duplicates(subset="date").sort_values("date")

        start_date = normalized["date"].min()
        end_date = normalized["date"].max()
        expected_dates = pd.date_range(start=start_date, end=end_date, freq="B")
        holidays = _nasdaq_holidays(start_date, end_date)
        ignored_holidays: List[str] = []
        if holidays:
            expected_dates = expected_dates.difference(holidays)
            ignored_holidays = [d.date().isoformat() for d in holidays]

        missing_dates = [
            d.date().isoformat() for d in expected_dates.difference(normalized["date"])
        ]

        missing_by_column = {
            col: int(normalized[col].isna().sum())
            for col in ["open", "high", "low", "close", "volume", "adj_close"]
        }

        status = "OK"
        if missing_dates or any(count > 0 for count in missing_by_column.values()):
            status = "NOT_OK"

        stats = {
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "rows": int(len(normalized)),
            "missing_dates": missing_dates,
            "missing_by_column": missing_by_column,
            "status": status,
            "ignored_holidays": ignored_holidays,
            "holiday_calendar_available": mcal is not None,
        }

        return normalized, stats

    def _persist(self, asset: str, df: pd.DataFrame, data_dir: Path) -> Dict:
        cleaned_df, stats = self._validate_data(df)

        safe_asset = asset.replace("/", "_").replace(" ", "_")
        safe_source = str(self.source).lower().replace(" ", "_")
        filename = (
            f"{safe_asset}_{safe_source}_1d_{stats['start_date'].replace('-', '')}_"
            f"{stats['end_date'].replace('-', '')}.csv"
        )
        data_path = data_dir / filename
        cleaned_df.to_csv(data_path, index=False)

        metadata = {
            "asset": asset,
            "source": self.source,
            "data_file": data_path.name,
            "start_date": stats["start_date"],
            "end_date": stats["end_date"],
            "rows": stats["rows"],
            "missing_dates": stats["missing_dates"],
            "missing_by_column": stats["missing_by_column"],
            "status": stats["status"],
            "generated_at": pd.Timestamp.utcnow().isoformat(),
        }

        metadata_path = data_path.with_suffix(".metadata.json")
        with metadata_path.open("w") as fh:
            json.dump(metadata, fh, indent=2)

        return metadata

    def _latest_metadata_path(self, asset: str, data_dir: Path) -> Optional[Path]:
        safe_asset = asset.replace("/", "_").replace(" ", "_")
        safe_source = str(self.source).lower().replace(" ", "_")
        candidates = sorted(data_dir.glob(f"{safe_asset}_{safe_source}_1d_*.metadata.json"))

        if not candidates:
            return None
        return max(candidates, key=lambda p: p.stat().st_mtime)

    @staticmethod
    def _print_summary(metadata: Dict, already_exists: bool = False) -> None:
        status = metadata["status"]
        headline = "Data Already Up-to-Date" if already_exists else "Data Saved"
        message = (
            f"Asset: {metadata['asset']}, Status: {headline}, {metadata['data_file']} "
            f"({metadata['rows']} rows, {metadata['start_date']} → {metadata['end_date']}, status={status})"
        )
        print(message)
