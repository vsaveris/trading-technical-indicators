"""
Trading-Technical-Indicators (tti) python library

File name: _training_data.py
    Implements the LSTMData class, that is used for preparing datasets for feeding a LSTM model.
"""

from typing import Iterator, List, Dict, Any, Optional
from pathlib import Path
from collections import defaultdict
import json
from dataclasses import asdict
import shutil
from tqdm import tqdm

import pandas as pd
import numpy as np

from ..data import OHLCV, MLData, DataSplitFactors, DatasetSize


class LSTMData(MLData):
    """
    Prepares LSTM-ready datasets (feature engineering, scaling, splitting, npz export).

    Args:
        ti_features (List[Dict[str, Any]]): List of TI specs, each with keys `ti` (indicator name) and `kwargs`
            (params).
        label_horizon (int): Lookahead horizon used to compute the log-return label.
        sequence_length (int): Length of each sliding window sequence (time-steps per sample).
        data_split (DataSplitFactors): Fractions for train/validation/test; must sum to 1.0.
        output_dir (Path): Target directory for parquet/intermediate files and final npz/index; must be empty or
            missing.
        display_progress (bool, default=False): Enable tqdm progress while processing input CSVs.

    Raises:
        RuntimeError: If output directory exists and is not empty.
        ValueError: When there is no `label` column in parquet data. When there is no scaler found for a dataset column.
    """

    _TEMP_SUB_DIR = "tmp"
    _METADATA_FILE = "metadata.json"
    _DATASET_INDEX_FILE = "dataset_index.json"

    def __init__(
        self,
        ti_features: List[Dict[str, Any]],
        label_horizon: int,
        sequence_length: int,
        data_split: DataSplitFactors,
        output_dir: Path,
        display_progress: bool = False,
    ):
        super().__init__()
        self._ti_features = ti_features
        self._label_horizon = label_horizon
        self._sequence_length = sequence_length
        self._data_split = data_split
        self._display_progress = display_progress

        if output_dir.exists():
            if any(output_dir.iterdir()):
                raise RuntimeError(f"Directory '{output_dir}' exists and is not empty.")

        output_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir = output_dir

        self._dataset_size = DatasetSize()
        self._scalers = defaultdict(dict)

        output_dir.joinpath(self._TEMP_SUB_DIR).mkdir(parents=True, exist_ok=True)

        self._errors = defaultdict(int)

    def create_data(self, input_csv_files: Iterator[Path]):
        """
        Build the dataset from raw CSV files: feature engineering, label creation, splitting, scaling, and npz export
        with accompanying metadata/index files.

        Args:
            input_csv_files (Iterator[Path]): Iterable of CSV paths (one per symbol) to ingest.

        Notes:
            - Writes intermediate parquet split files under `output_dir/tmp`.
            - Writes per-split npz files and `dataset_index.json` under `output_dir`.
            - Writes `metadata.json` with scaler and config metadata under `output_dir`.
            - Removes the temporary parquet directory when finished.
        """
        stats = defaultdict(lambda: defaultdict(float))

        for file in tqdm(
            input_csv_files, desc="files", unit="file(s)", disable=not self._display_progress
        ):
            features_df = self._create_features(file)

            if features_df is None:
                self._errors["SkippingCSVFile[EmptyFeaturesDataframe]"] += 1
                continue

            data_df = self._create_labels(features_df)
            train_df, _, _ = self._create_splits(file.stem, data_df)

            # For scalers computations, we use only the training data.
            if train_df is not None:
                for column in train_df.columns:
                    data = train_df[column].values
                    stats[column]["sum"] += data.sum(axis=0)
                    stats[column]["sum_squared"] += (data**2).sum(axis=0)
                    stats[column]["count"] += data.shape[0]

        self._compute_scalers(stats)
        self._save_metadata_file()

        self._create_npz_sequences()

        # Remove parquet files
        shutil.rmtree(self._output_dir.joinpath(self._TEMP_SUB_DIR))

    def _create_npz_sequences(self) -> None:
        """
        Convert split Parquet files into per-stock npz sequence files, with lazy-loading index.
        """
        index: Dict[str, List[Dict[str, Any]]] = {
            "train": [],
            "validation": [],
            "test": [],
        }

        for split in ["train", "validation", "test"]:
            (self._output_dir / split).mkdir(exist_ok=True)

        def process_split(split_name: str):
            split_dir = self._output_dir / split_name
            pattern = f"{split_name}_*.parquet"

            for parquet_path in sorted(self._output_dir.joinpath(self._TEMP_SUB_DIR).glob(pattern)):
                symbol = parquet_path.stem.split("_", 1)[1]

                df = pd.read_parquet(parquet_path)

                if "label" not in df.columns:
                    raise ValueError(f"{parquet_path} has no 'label' column")

                feature_cols = [c for c in df.columns if c != "label"]

                # Scale using global scalers
                df_scaled = df.copy()
                for col in df_scaled.columns:
                    if col not in self._scalers:
                        raise ValueError(f"No scaler found for column '{col}'")
                    mean = self._scalers[col]["mean"]
                    std = self._scalers[col]["std"] or 1e-8
                    df_scaled[col] = (df_scaled[col] - mean) / std

                x = df_scaled[feature_cols].to_numpy(dtype=np.float32)
                y = df_scaled["label"].to_numpy(dtype=np.float32)

                x_seq, y_seq = self._make_lstm_sequences(x, y)

                n_seq = x_seq.shape[0]
                if n_seq == 0:
                    self._errors["SkippingParquetFile[NoSequences]"] += 1
                    continue

                out_file = split_dir / f"{symbol}.npz"
                np.savez_compressed(str(out_file), X=x_seq, y=y_seq)

                index[split_name].append(
                    {
                        "file": str(out_file.relative_to(self._output_dir)),
                        "num_samples": int(n_seq),
                        "symbol": symbol,
                    }
                )

        process_split("train")
        process_split("validation")
        process_split("test")

        index_payload = {
            "index": index,
            "sequence_length": self._sequence_length,
            "label_col": "label",
            "dataset_size": {
                "train_n_sequences": sum([x["num_samples"] for x in index["train"]]),
                "validation_n_sequences": sum([x["num_samples"] for x in index["validation"]]),
                "test_n_sequences": sum([x["num_samples"] for x in index["test"]]),
            },
        }

        with open(self._output_dir / self._DATASET_INDEX_FILE, "w") as f:
            json.dump(index_payload, f, indent=4)

    def _make_lstm_sequences(self, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Build sliding-window sequences per stock, per split.

        x: (T, n_features)
        y: (T,) or (T, 1)
        """
        t = x.shape[0]
        if t <= self._sequence_length:
            return (
                np.empty((0, self._sequence_length, x.shape[1]), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
            )

        y = y.reshape(-1)
        x_seq, y_seq = [], []

        for i in range(self._sequence_length - 1, t):
            x_seq.append(x[i - self._sequence_length + 1 : i + 1])
            y_seq.append(y[i])

        return np.array(x_seq, dtype=np.float32), np.array(y_seq, dtype=np.float32)

    def _compute_scalers(self, stats_per_column: Dict[str, Dict[str, float]]):
        for column, col_stats in stats_per_column.items():
            mean = col_stats["sum"] / col_stats["count"]

            variance = (col_stats["sum_squared"] / col_stats["count"]) - mean**2
            variance = np.maximum(variance, 1e-8)  # Avoid division by zero
            std = np.sqrt(variance)

            self._scalers[column] = {"mean": float(mean), "std": float(std)}

    def _save_metadata_file(self):
        with open(self._output_dir.joinpath(self._METADATA_FILE), "w") as f:
            json.dump(
                self._scalers
                | asdict(self._dataset_size)
                | {
                    "ti_features": self._ti_features,
                    "label_horizon": self._label_horizon,
                    "sequence_length": self._sequence_length,
                    "data_split": asdict(self._data_split),
                    "errors": self._errors,
                },
                f,
                indent=4,
            )

    def _create_splits(self, file_stem: str, df: pd.DataFrame):
        df = df.copy()

        if df.shape[0] < self._sequence_length:
            return None, None, None

        train_len = int(df.shape[0] * self._data_split.train)
        validation_len = int(df.shape[0] * self._data_split.validation)
        test_len = df.shape[0] - train_len - validation_len

        if min(train_len, validation_len, test_len) >= self._sequence_length:
            df.iloc[:train_len].to_parquet(
                self._output_dir.joinpath(self._TEMP_SUB_DIR).joinpath(f"train_{file_stem}.parquet")
            )
            df.iloc[train_len : train_len + validation_len].to_parquet(
                self._output_dir.joinpath(self._TEMP_SUB_DIR).joinpath(
                    f"validation_{file_stem}.parquet"
                )
            )
            df.iloc[train_len + validation_len :].to_parquet(
                self._output_dir.joinpath(self._TEMP_SUB_DIR).joinpath(f"test_{file_stem}.parquet")
            )

            self._dataset_size.train_n_samples += train_len
            self._dataset_size.validation_n_samples += validation_len
            self._dataset_size.test_n_samples += test_len

            return (
                df.iloc[:train_len],
                df.iloc[train_len : train_len + validation_len],
                df.iloc[train_len + validation_len :],
            )

        # Not enough data for validation and test splits. Use these data only for training.
        else:
            df.to_parquet(
                self._output_dir.joinpath(self._TEMP_SUB_DIR).joinpath(f"train_{file_stem}.parquet")
            )

            self._dataset_size.train_n_samples += df.shape[0]
            self._errors["SkippingValTestSplits[NotEnoughData]"] += 1

            return df, None, None

    def _create_features(self, input_csv_file: Path) -> Optional[pd.DataFrame]:
        df = pd.read_csv(
            input_csv_file, parse_dates=["date"], date_format="%Y-%m-%d", index_col="date"
        )
        df.sort_index(inplace=True)

        # Add 1 to the volume column, to avoid inf or -inf values in indicators where volume is denominator and 0.
        df["volume"] = df["volume"] + 1

        # Add features from OHLCV data and drop not needed labels
        data_df = OHLCV(df).df

        # Add technical indicators
        data_df = self._add_indicators(data_df)

        # Drop not needed columns and rows with at least one NaN
        if data_df is not None:
            data_df.drop(columns=["close"], inplace=True)
            data_df.dropna(inplace=True)

        return data_df

    def _create_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["label"] = np.log(df["adj_close"].shift(-self._label_horizon) / df["adj_close"])

        df.dropna(inplace=True)

        return df

    def _add_indicators(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        df = df.copy()

        for i, indicator in enumerate(self._ti_features):
            try:
                results = self._compute_ti(df, indicator["ti"], **indicator["kwargs"])

                if isinstance(results, pd.Series):
                    results = results.to_frame(name="value")

            except Exception:  # noqa
                self._errors[f"SkippingCSVFile[Failed{indicator['ti']}]"] += 1
                return None

            for column in results.columns:
                df[f"ti_{i}_{column}"] = results[column]

        return df
