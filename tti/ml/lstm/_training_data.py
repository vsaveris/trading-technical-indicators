"""
Utilities for building LSTM-ready training datasets from historical OHLCV CSV files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

from tti import indicators
from tti.utils.constants import ALL_TI_FEATURES
from tti.utils.exceptions import NotEnoughInputData


LABEL_TO_ID = {"BUY": 0, "HOLD": 1, "SELL": 2}
ID_TO_LABEL = {v: k for k, v in LABEL_TO_ID.items()}


@dataclass
class DatasetSplit:
    X: np.ndarray
    y: np.ndarray


@dataclass
class LSTMDataset:
    train: DatasetSplit
    test: Optional[DatasetSplit]
    feature_names: List[str]
    scaler: Dict[str, Tuple[float, float]]
    params: Dict[str, any] | None = None


def _load_csv(path: Path) -> pd.DataFrame:
    # Parse whichever date column is present
    parse_cols = []
    peek = pd.read_csv(path, nrows=0)
    if "date" in peek.columns:
        parse_cols.append("date")
    if "Date" in peek.columns:
        parse_cols.append("Date")
    df = pd.read_csv(path, parse_dates=parse_cols if parse_cols else None)

    # Normalize column names to lower case
    df.columns = [c.lower() for c in df.columns]
    if "date" not in df.columns:
        raise ValueError(f"CSV {path} missing 'date' column.")
    df = df.sort_values("date").reset_index(drop=True)
    return df


def _compute_indicators(df: pd.DataFrame, features: Sequence[Dict]) -> pd.DataFrame:
    """
    For each indicator definition in ALL_TI_FEATURES, compute values and append as columns.
    """
    ti_input = df.set_index("date")[["open", "high", "low", "close", "volume"]]

    for item in features:
        ti_name = item["ti"]
        kwargs = item.get("kwargs", {})
        cls = getattr(indicators, ti_name)
        try:
            ti = cls(input_data=ti_input, **kwargs)
            ti_df = ti.getTiData()
            prefixed = ti_df.add_prefix(f"{ti_name}_").reset_index(drop=True)
            df = pd.concat([df.reset_index(drop=True), prefixed], axis=1)
        except NotEnoughInputData:
            # Skip indicators that cannot be computed on very short series.
            print(
                f"[build_lstm_dataset] Skipping indicator {ti_name} due to insufficient data ({len(df)} rows)."
            )
        except Exception as exc:
            print(f"[build_lstm_dataset] Skipping indicator {ti_name} due to error: {exc}")

    return df


def _build_labels(df: pd.DataFrame, lookahead: int, threshold: float) -> pd.Series:
    """
    Create BUY/SELL/HOLD labels based on forward return over `lookahead` days.
    """
    future = df["adj_close"].shift(-lookahead)
    forward_ret = (future - df["adj_close"]) / df["adj_close"]

    labels = np.where(
        forward_ret >= threshold, "BUY", np.where(forward_ret <= -threshold, "SELL", "HOLD")
    )
    return pd.Series(labels, index=df.index)


def _standardize(train_df: pd.DataFrame, test_df: Optional[pd.DataFrame], feature_cols: List[str]):
    scaler: Dict[str, Tuple[float, float]] = {}
    for col in feature_cols:
        values = np.asarray(train_df[col], dtype=np.float64)
        if values.size == 0:
            raise ValueError(f"No data available to standardize for feature '{col}'.")
        mean_val = float(values.mean())
        std_val = float(values.std())
        if std_val == 0:
            std_val = 1.0  # avoid division by zero; feature is constant so scaling to zero-mean is harmless
        scaler[col] = (mean_val, std_val)
        train_df[col] = (train_df[col].astype(float) - mean_val) / std_val
        if test_df is not None:
            test_df[col] = (test_df[col].astype(float) - mean_val) / std_val
    return scaler


def _make_sequences(df: pd.DataFrame, feature_cols: List[str], labels: pd.Series, seq_len: int):
    X_list = []
    y_list = []
    values = df[feature_cols].to_numpy(dtype=np.float32)
    label_ids = labels.map(LABEL_TO_ID).to_numpy(dtype=np.int64)

    for i in range(len(df) - seq_len):
        X_list.append(values[i : i + seq_len])
        y_list.append(label_ids[i + seq_len])

    if not X_list:
        return None, None

    return np.stack(X_list), np.array(y_list)


def build_lstm_dataset(
    data_dir: Path,
    lookahead: int = 5,
    threshold: float = 0.02,
    sequence_length: int = 30,
    holdout_rows: int = 0,
    indicators_to_use: Sequence[Dict] = ALL_TI_FEATURES,
    min_rows: int = 0,
    work_dir: Optional[Path] = None,
    chunk_sequences: int = 50000,
) -> LSTMDataset:
    """
    Build an LSTM-ready dataset from all CSVs in a directory.

    Args:
        data_dir: Directory containing historical CSVs.
        lookahead: Days to look ahead for generating labels.
        threshold: Minimum forward return magnitude to emit BUY/SELL, else HOLD.
        sequence_length: Number of time steps in each input sequence.
        holdout_rows: If >0, reserve the last N labeled rows from each asset for testing.
        indicators_to_use: Indicator definitions (defaults to ALL_TI_FEATURES).
        min_rows: If >0, skip CSV files with fewer raw rows than this threshold.
        work_dir: Directory used for temporary chunks and final memmaps. Defaults to data_dir / ".lstm_cache".
        chunk_sequences: Flush intermediate train/test sequences to disk every N sequences to avoid high RAM.
    """
    work_dir = Path(work_dir) if work_dir else Path(data_dir) / ".lstm_cache"
    work_dir.mkdir(parents=True, exist_ok=True)

    train_chunks_X: List[Path] = []
    train_chunks_y: List[Path] = []
    test_chunks_X: List[Path] = []
    test_chunks_y: List[Path] = []
    train_chunk_counts: List[int] = []
    test_chunk_counts: List[int] = []
    train_buffer_X: List[np.ndarray] = []
    train_buffer_y: List[np.ndarray] = []
    test_buffer_X: List[np.ndarray] = []
    test_buffer_y: List[np.ndarray] = []
    train_total = 0
    test_total = 0
    feature_cols: List[str] = []
    scaler: Dict[str, Tuple[float, float]] = {}

    def _flush(
        buffer_X,
        buffer_y,
        prefix: str,
        chunks_X: List[Path],
        chunks_y: List[Path],
        counts: List[int],
        total: int,
    ):
        if not buffer_X:
            return total
        arr_X = np.concatenate(buffer_X, axis=0)
        arr_y = np.concatenate(buffer_y, axis=0)
        chunk_idx = len(chunks_X)
        path_X = work_dir / f"{prefix}_X_{chunk_idx}.npy"
        path_y = work_dir / f"{prefix}_y_{chunk_idx}.npy"
        np.save(path_X, arr_X)
        np.save(path_y, arr_y)
        chunks_X.append(path_X)
        chunks_y.append(path_y)
        counts.append(arr_X.shape[0])
        total += arr_X.shape[0]
        buffer_X.clear()
        buffer_y.clear()
        return total

    def _assemble(chunks: List[Path], counts: List[int], prefix: str) -> Optional[np.ndarray]:
        if not chunks:
            return None
        total_rows = sum(counts)
        first = np.load(chunks[0], mmap_mode="r")
        shape = (total_rows, *first.shape[1:])
        mmap_path = work_dir / f"{prefix}_all.npy"
        mmap_arr = np.lib.format.open_memmap(mmap_path, mode="w+", dtype=first.dtype, shape=shape)
        offset = 0
        for path, count in zip(chunks, counts):
            chunk = np.load(path, mmap_mode="r")
            mmap_arr[offset : offset + count] = chunk
            offset += count
        mmap_arr.flush()
        # remove chunk files
        for path in chunks:
            path.unlink(missing_ok=True)
        return np.load(mmap_path, mmap_mode="r+")

    csv_files = sorted(Path(data_dir).glob("*.csv"))
    if not csv_files:
        raise ValueError(f"No CSV files found in {data_dir}")

    total_files = len(csv_files)
    processed_files = 0
    skipped_files = 0
    processed_rows = 0
    skipped_rows = 0

    iterator: Iterable[Path] = csv_files
    if tqdm is not None:
        iterator = tqdm(csv_files, desc="[build_lstm_dataset] CSV files", unit="file")

    for csv_path in iterator:
        df = _load_csv(csv_path)
        raw_rows = len(df)
        if min_rows and raw_rows < min_rows:
            skipped_files += 1
            skipped_rows += raw_rows
            continue
        # Ensure required columns exist
        required = {"open", "high", "low", "close", "adj_close", "volume"}
        if missing := required.difference(df.columns):
            raise ValueError(f"Missing columns {missing} in {csv_path}")

        try:
            df = _compute_indicators(df, indicators_to_use)
        except NotEnoughInputData:
            skipped_files += 1
            skipped_rows += raw_rows
            continue
        except Exception:
            skipped_files += 1
            skipped_rows += raw_rows
            continue

        # Drop columns that are entirely NaN to avoid wiping out all rows
        non_empty_cols = [c for c in df.columns if not pd.isna(df[c]).to_numpy().all()]
        df = df[non_empty_cols]

        labels = _build_labels(df, lookahead=lookahead, threshold=threshold)
        # Drop trailing rows without labels
        cutoff = len(df) - lookahead
        df = df.iloc[:cutoff].reset_index(drop=True)
        labels = labels.iloc[:cutoff].reset_index(drop=True)

        # Drop rows with any NaNs across features/labels
        combined = pd.concat([df, labels.rename("label")], axis=1)
        combined = combined.dropna()
        labels = combined.pop("label").reset_index(drop=True)
        df = combined.reset_index(drop=True)

        if len(df) == 0:
            skipped_files += 1
            skipped_rows += raw_rows
            continue

        if len(df) <= sequence_length:
            skipped_files += 1
            skipped_rows += raw_rows
            continue

        # Determine train/test split
        if holdout_rows > 0:
            if len(df) <= holdout_rows:
                skipped_files += 1
                skipped_rows += raw_rows
                continue
            train_df = df.iloc[:-holdout_rows].copy()
            test_df = df.iloc[-holdout_rows:].copy()
            train_labels = labels.iloc[:-holdout_rows].copy()
            test_labels = labels.iloc[-holdout_rows:].copy()
        else:
            train_df = df.copy()
            test_df = None
            train_labels = labels.copy()
            test_labels = None

        if len(train_df) <= sequence_length:
            skipped_files += 1
            skipped_rows += raw_rows
            continue

        # Initialize feature columns once from the first asset
        if not feature_cols:
            numeric_cols = train_df.select_dtypes(exclude=["object"]).columns.tolist()
            feature_cols = [c for c in numeric_cols if c != "date"]
        else:
            # Skip asset if required feature columns are missing
            missing = [c for c in feature_cols if c not in train_df.columns]
            if missing:
                skipped_files += 1
                skipped_rows += raw_rows
                continue

        # Standardize using train stats for current asset
        asset_scaler = _standardize(train_df, test_df, feature_cols)
        scaler.update({f"{csv_path.name}:{k}": v for k, v in asset_scaler.items()})

        train_X, train_y = _make_sequences(train_df, feature_cols, train_labels, sequence_length)
        if train_X is None:
            skipped_files += 1
            skipped_rows += raw_rows
            continue
        processed_files += 1
        processed_rows += raw_rows
        train_buffer_X.append(train_X)
        train_buffer_y.append(train_y)
        if sum(x.shape[0] for x in train_buffer_X) >= chunk_sequences:
            train_total = _flush(
                train_buffer_X,
                train_buffer_y,
                "train",
                train_chunks_X,
                train_chunks_y,
                train_chunk_counts,
                train_total,
            )

        if test_df is not None and len(test_df) > sequence_length:
            test_X, test_y = _make_sequences(test_df, feature_cols, test_labels, sequence_length)
            if test_X is not None:
                test_buffer_X.append(test_X)
                test_buffer_y.append(test_y)
                if sum(x.shape[0] for x in test_buffer_X) >= max(1, chunk_sequences // 2):
                    test_total = _flush(
                        test_buffer_X,
                        test_buffer_y,
                        "test",
                        test_chunks_X,
                        test_chunks_y,
                        test_chunk_counts,
                        test_total,
                    )

    # Flush remaining buffers
    train_total = _flush(
        train_buffer_X,
        train_buffer_y,
        "train",
        train_chunks_X,
        train_chunks_y,
        train_chunk_counts,
        train_total,
    )
    test_total = _flush(
        test_buffer_X,
        test_buffer_y,
        "test",
        test_chunks_X,
        test_chunks_y,
        test_chunk_counts,
        test_total,
    )

    if train_total == 0:
        raise ValueError("No training data created; all assets were skipped.")

    train_X_mm = _assemble(train_chunks_X, train_chunk_counts, "train_X")
    train_y_mm = _assemble(train_chunks_y, train_chunk_counts, "train_y")
    if train_y_mm is None:
        raise ValueError("Failed to assemble training labels.")

    test_split = None
    if test_chunks_X:
        test_X_mm = _assemble(test_chunks_X, test_chunk_counts, "test_X")
        test_y_mm = _assemble(test_chunks_y, test_chunk_counts, "test_y")
        if test_X_mm is not None and test_y_mm is not None:
            test_split = DatasetSplit(X=test_X_mm, y=test_y_mm)

    train_split = DatasetSplit(X=train_X_mm, y=train_y_mm)

    total_rows_count = processed_rows + skipped_rows
    print(
        f"[build_lstm_dataset] Train sequences: {train_split.X.shape}, labels: {train_split.y.shape}"
        + (f", Test: {test_split.X.shape}" if test_split else ", Test: None")
        + f". Processed files: {processed_files}/{total_files} ({processed_rows} rows)."
        + f" Skipped files: {skipped_files} ({skipped_rows} rows)."
        + f" Total rows read: {total_rows_count}."
    )

    return LSTMDataset(
        train=train_split,
        test=test_split,
        feature_names=feature_cols,
        scaler=scaler,
        params={
            "lookahead": lookahead,
            "threshold": threshold,
            "sequence_length": sequence_length,
            "holdout_rows": holdout_rows,
        },
    )


def save_dataset(dataset: LSTMDataset, out_dir: Path) -> None:
    """
    Persist an LSTMDataset to disk as numpy arrays and JSON metadata.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "train_X.npy", dataset.train.X)
    np.save(out_dir / "train_y.npy", dataset.train.y)
    if dataset.test:
        np.save(out_dir / "test_X.npy", dataset.test.X)
        np.save(out_dir / "test_y.npy", dataset.test.y)
    meta = {
        "feature_names": dataset.feature_names,
        "scaler": dataset.scaler,
        "params": dataset.params,
    }
    with open(out_dir / "meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)


def load_dataset(in_dir: Path) -> LSTMDataset:
    """
    Load an LSTMDataset previously saved with save_dataset.
    """
    in_dir = Path(in_dir)
    train_X = np.load(in_dir / "train_X.npy", mmap_mode="r")
    train_y = np.load(in_dir / "train_y.npy", mmap_mode="r")
    test_X_path = in_dir / "test_X.npy"
    test_y_path = in_dir / "test_y.npy"
    test_split = None
    if test_X_path.exists() and test_y_path.exists():
        test_split = DatasetSplit(
            X=np.load(test_X_path, mmap_mode="r"), y=np.load(test_y_path, mmap_mode="r")
        )
    with open(in_dir / "meta.json") as fh:
        meta = json.load(fh)
    return LSTMDataset(
        train=DatasetSplit(X=train_X, y=train_y),
        test=test_split,
        feature_names=meta["feature_names"],
        scaler=meta["scaler"],
        params=meta.get("params"),
    )


def prepare_prediction_window(
    df: pd.DataFrame,
    dataset: LSTMDataset,
    sequence_length: Optional[int] = None,
    indicators_to_use: Optional[Sequence[Dict]] = None,
) -> np.ndarray:
    """
    Prepare a single prediction window from raw OHLCV DataFrame using training metadata.

    Args:
        df: DataFrame containing at least OHLCV columns (open, high, low, close, adj_close, volume) and 'date'.
            Must be sorted ascending.
        dataset: LSTMDataset with feature_names and scaler loaded (via load_dataset).
        sequence_length: If provided, overrides dataset.params['sequence_length']; otherwise required in params.
        indicators_to_use: Optional indicator definitions. If None, uses dataset.params.get("indicators_to_use")
            or falls back to ALL_TI_FEATURES.

    Returns:
        np.ndarray of shape (1, sequence_length, n_features) ready for model.predict.
    """
    seq_len = sequence_length or (dataset.params["sequence_length"] if dataset.params else None)
    if seq_len is None:
        raise ValueError("sequence_length not provided and not found in dataset.params")

    # Normalize column names
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    df = df.sort_values("date")

    # Compute indicators if not already present
    indicators_def = (
        indicators_to_use
        or (dataset.params.get("indicators_to_use") if dataset.params else None)
        or ALL_TI_FEATURES
    )
    # If indicators are already present, skip recompute
    has_any_indicator = any(
        col not in {"date", "open", "high", "low", "close", "adj_close", "volume"}
        for col in df.columns
    )
    if not has_any_indicator:
        required = {"open", "high", "low", "close", "adj_close", "volume"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Missing required columns for indicator computation: {missing}")
        df = _compute_indicators(df, indicators_def)

    # Ensure all feature columns exist; fill missing with NaN then scale.
    for col in dataset.feature_names:
        if col not in df.columns:
            df[col] = np.nan

    for col in dataset.feature_names:
        m, s = (
            dataset.scaler.get(col, (0.0, 1.0)) if isinstance(dataset.scaler, dict) else (0.0, 1.0)
        )
        df[col] = (df[col].astype(float) - m) / (s if s != 0 else 1.0)

    features = df[dataset.feature_names].to_numpy(dtype=np.float32)
    if len(features) < seq_len:
        raise ValueError(
            f"Not enough rows for a prediction window; need at least {seq_len}, got {len(features)}"
        )
    window = features[-seq_len:]
    # Fail if any NaN is present in the target window (pre-scaling values considered in window slice)
    if df[dataset.feature_names].iloc[-seq_len:].isna().any().any():
        nan_cols = (
            df[dataset.feature_names]
            .columns[df[dataset.feature_names].iloc[-seq_len:].isna().any()]
            .tolist()
        )
        raise ValueError(
            f"NaN values present in the prediction window before scaling: {nan_cols[:10]}{'...' if len(nan_cols)>10 else ''}"
        )
    # Fail if any NaN remains after scaling
    if np.isnan(window).any():
        raise ValueError(
            "NaN values present in prediction window after preprocessing; cannot predict."
        )
    return window.reshape(1, seq_len, len(dataset.feature_names))
