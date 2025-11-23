"""
Trading-Technical-Indicators (tti) python library

File name: _utils.py
    Implements useful classes for the tti.ml.data package.
"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class DataSplitFactors:
    train: float
    validation: float
    test: float

    def __post_init__(self):
        if (split_sum := self.train + self.validation + self.test) != 1.0:
            raise ValueError(
                f"Invalid data split sum(train, validation, test) = {split_sum} != 1.0"
            )


@dataclass
class DatasetSize:
    train_n_samples: int = 0
    validation_n_samples: int = 0
    test_n_samples: int = 0


class DatasetSplit(Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"
