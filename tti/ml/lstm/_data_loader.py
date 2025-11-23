"""
Trading-Technical-Indicators (tti) python library

File name: _data_loader.py
    Implements the dataloader interface that is used when training a LSTM model.
"""

from pathlib import Path
import json
import bisect

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

from ..data import DatasetSplit


class LazyDatasetLoader(Dataset):
    """
    Lazy-loading Dataset for sequences stored in per-stock npz files.

    Args:
        root_dir (Path): The root dir of the dataset that contains the npz files and the _DATASET_INDEX_FILE.
            (created by tti/ml/lstm/_training_data.py).
        split (DatasetSplit): The dataset split to load.

    Raises:
        FileNotFoundError: If _DATASET_INDEX_FILE is not found in the provided dataset dir.
        RuntimeError: If no data found for the given split.
        ValueError: If split is not found in the dataset index file.

    Each entry points to a per-stock npz with arrays:
      - X: shape (n_sequences, sequence_length, n_features)
      - y: shape (n_sequences,)
    """

    _DATASET_INDEX_FILE = "dataset_index.json"

    def __init__(self, root_dir: Path, split: DatasetSplit):
        super().__init__()
        self.root_dir = root_dir

        with open(root_dir / self._DATASET_INDEX_FILE, "r") as f:
            payload = json.load(f)

        index = payload["index"]
        if split.value not in index:
            raise ValueError(f"Split '{split}' not found in dataset_index.json")

        self.entries = index[split.value]  # list of {file, num_samples, symbol}

        if not self.entries:
            raise RuntimeError(f"No entries found for split '{split}'")

        counts = [e["num_samples"] for e in self.entries]
        self.cumulative_counts = np.cumsum(counts).tolist()
        self.total_samples = self.cumulative_counts[-1]

        # per-dataset simple cache of last loaded file
        self._cache_path = None
        self._cache_X = None
        self._cache_y = None

    def __len__(self):
        return self.total_samples

    def _load_file(self, rel_path: str):
        full_path = str(self.root_dir / rel_path)
        if full_path == self._cache_path and self._cache_X is not None:
            return self._cache_X, self._cache_y

        data = np.load(full_path)
        x = data["X"]
        y = data["y"]

        self._cache_path = full_path
        self._cache_X = x
        self._cache_y = y
        return x, y

    def __getitem__(self, idx: int):
        if idx < 0 or idx >= self.total_samples:
            raise IndexError(idx)

        file_idx = bisect.bisect_right(self.cumulative_counts, idx)
        start = 0 if file_idx == 0 else self.cumulative_counts[file_idx - 1]
        offset = idx - start

        entry = self.entries[file_idx]
        rel_path = entry["file"]

        x, y = self._load_file(rel_path)

        x_seq = x[offset]  # (seq_len, n_features)
        y_seq = y[offset]  # scalar

        x_tensor = torch.from_numpy(x_seq).float()
        y_tensor = torch.tensor(y_seq, dtype=torch.float32)

        return x_tensor, y_tensor


def build_dataloader(
    root_dir: Path,
    batch_size: int,
    split: DatasetSplit,
    shuffle: bool,
    drop_last: bool,
    num_workers: int = 0,
) -> DataLoader:
    """
    Prepares a dataloader for the given dataset and parameters.
    Args:
        root_dir (Path): The root dir of the dataset.
        batch_size (int): The size of batch.
        split (DatasetSplit): The dataset split to load.
        shuffle (bool): Shuffle data in split. Recommended to set True for training data.
        drop_last (bool): If True, creates only full batches. Recommended for training data.
        num_workers (int, default=0): The number of workers to use for loading data. 0 means that the data will be
            loaded in the main process.

    Returns:
        DataLoader: The initialised dataloader.
    """
    return DataLoader(
        LazyDatasetLoader(root_dir=root_dir, split=split),
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers,
    )
