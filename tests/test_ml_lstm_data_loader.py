"""
Trading-Technical-Indicators (tti) python library

File name: test_ml_downloader.py
    tti.ml.lstm._data_loader module unit tests.
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import torch

from tti.ml.data import DatasetSplit
from tti.ml.lstm import LazyDatasetLoader, build_dataloader


class TestLazyDatasetLoader(unittest.TestCase):
    def test_missing_index_file_raises(self):
        with TemporaryDirectory() as tmpdir:
            with self.assertRaises(FileNotFoundError):
                LazyDatasetLoader(Path(tmpdir), DatasetSplit.TRAIN)

    def test_empty_split_raises(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            payload = {"index": {DatasetSplit.TRAIN.value: []}}
            (root / "dataset_index.json").write_text(json.dumps(payload))

            with self.assertRaises(RuntimeError):
                LazyDatasetLoader(root, DatasetSplit.TRAIN)

    def test_split_not_found_raises(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            payload = {"index": {DatasetSplit.TRAIN.value: []}}
            (root / "dataset_index.json").write_text(json.dumps(payload))

            with self.assertRaises(ValueError):
                LazyDatasetLoader(root, DatasetSplit.VALIDATION)

    def test_getitem_returns_expected_shapes(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            x = np.ones((2, 3, 4), dtype=np.float32)
            y = np.array([1.0, -1.0], dtype=np.float32)

            npz_rel = Path("train") / "AAA.npz"
            (root / "train").mkdir()
            np.savez_compressed(root / npz_rel, X=x, y=y)

            payload = {
                "index": {
                    DatasetSplit.TRAIN.value: [
                        {"file": str(npz_rel), "num_samples": len(y), "symbol": "AAA"}
                    ]
                }
            }
            (root / "dataset_index.json").write_text(json.dumps(payload))

            loader = LazyDatasetLoader(root, DatasetSplit.TRAIN)

            self.assertEqual(len(loader), 2)

            x_tensor, y_tensor = loader[0]
            self.assertEqual(tuple(x_tensor.shape), (3, 4))
            self.assertTrue(torch.is_tensor(y_tensor))
            self.assertEqual(y_tensor.dim(), 0)  # scalar target
            self.assertAlmostEqual(y_tensor.item(), 1.0)

    def test_get_dataloader_batches(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            x = np.stack([np.zeros((2, 2), dtype=np.float32), np.ones((2, 2), dtype=np.float32)])
            y = np.array([0.0, 1.0], dtype=np.float32)

            npz_rel = Path("train") / "BBB.npz"
            (root / "train").mkdir()
            np.savez_compressed(root / npz_rel, X=x, y=y)

            payload = {
                "index": {
                    DatasetSplit.TRAIN.value: [
                        {"file": str(npz_rel), "num_samples": len(y), "symbol": "BBB"}
                    ]
                }
            }
            (root / "dataset_index.json").write_text(json.dumps(payload))

            dl = build_dataloader(
                root_dir=root,
                batch_size=2,
                split=DatasetSplit.TRAIN,
                shuffle=False,
                drop_last=False,
            )

            batch_x, batch_y = next(iter(dl))

            self.assertEqual(tuple(batch_x.shape), (2, 2, 2))
            self.assertEqual(tuple(batch_y.shape), (2,))
            self.assertTrue(torch.allclose(batch_y, torch.tensor([0.0, 1.0], dtype=torch.float32)))


if __name__ == "__main__":
    unittest.main()
