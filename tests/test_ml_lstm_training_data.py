"""
Trading-Technical-Indicators (tti) python library

File name: test_ml_lstm_training_data.py
    tti.ml.lstm._training_data module unit tests.
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from tti.ml.data import DataSplitFactors
from tti.ml.lstm import LSTMData


class TestLSTMData(unittest.TestCase):
    def _make_csv(self, path: Path, rows: int = 100):
        dates = pd.date_range("2020-01-01", periods=rows, freq="D")
        base = np.arange(rows, dtype=float)
        volume = 1000.0 + 10.0 * np.sin(
            np.linspace(0, 10, rows)
        )  # avoid constant volume (zscore NaNs)
        df = pd.DataFrame(
            {
                "date": dates,
                "open": base + 10.0,
                "high": base + 11.0,
                "low": base + 9.0,
                "close": base + 10.5,
                "adj_close": base + 10.5,
                "volume": volume,
            }
        )
        df.to_csv(path, index=False, date_format="%Y-%m-%d")

    def test_create_data_generates_outputs(self):
        with TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            out_dir = Path(tmpdir) / "out"
            data_dir.mkdir()

            csv_path = data_dir / "AAA.csv"
            self._make_csv(csv_path, rows=100)

            builder = LSTMData(
                ti_features=[],  # no extra indicators
                label_horizon=1,
                sequence_length=5,
                data_split=DataSplitFactors(1.0, 0.0, 0.0),
                output_dir=out_dir,
                display_progress=False,
            )

            builder.create_data(input_csv_files=iter([csv_path]))

            index_path = out_dir / "dataset_index.json"
            metadata_path = out_dir / "metadata.json"
            train_dir = out_dir / "train"
            tmp_dir = out_dir / builder._TEMP_SUB_DIR

            self.assertTrue(index_path.exists())
            self.assertTrue(metadata_path.exists())
            self.assertTrue(train_dir.exists())
            self.assertFalse(tmp_dir.exists(), "temporary parquet directory should be removed")

            dataset_index = json.loads(index_path.read_text())
            train_entries = dataset_index["index"]["train"]
            self.assertGreater(len(train_entries), 0, "expected at least one train npz file")
            self.assertGreater(dataset_index["dataset_size"]["train_n_sequences"], 0)

            npz_files = list(train_dir.glob("*.npz"))
            self.assertGreater(len(npz_files), 0)

            # verify shapes inside npz
            npz = np.load(npz_files[0])
            self.assertEqual(npz["X"].ndim, 3)
            self.assertEqual(npz["y"].ndim, 1)
            self.assertEqual(npz["X"].shape[0], npz["y"].shape[0])

            metadata = json.loads(metadata_path.read_text())
            self.assertEqual(metadata["sequence_length"], 5)
            self.assertEqual(metadata["label_horizon"], 1)
            self.assertIn("ti_features", metadata)
            self.assertIn("train_n_samples", metadata)


if __name__ == "__main__":
    unittest.main()
