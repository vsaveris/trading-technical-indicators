"""
Base model interface for ML models used in the tti package.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

import numpy as np


class BaseModel(ABC):
    """Abstract base class for ML models."""

    @abstractmethod
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs) -> Any:
        """
        Train the model.

        Args:
            X_train: np.ndarray of shape (n_samples, seq_len, n_features)
            y_train: np.ndarray of shape (n_samples,)
        Returns:
            Training history or metrics.
        """

    @abstractmethod
    def predict(self, X: np.ndarray, **kwargs) -> np.ndarray:
        """
        Run inference and return class probabilities or logits.
        """

    @abstractmethod
    def save_checkpoint(self, path: Path) -> None:
        """
        Persist model weights and configuration to disk.
        """

    @classmethod
    @abstractmethod
    def load_checkpoint(cls, path: Path, **kwargs) -> "BaseModel":
        """
        Restore a model from a checkpoint file.
        """

    @abstractmethod
    def simulate(self, X: np.ndarray, prices: np.ndarray, **kwargs) -> Tuple[float, list]:
        """
        Run a simple trading simulation over the provided features and prices.

        Returns:
            (final_return_multiple, decisions_list)
        """
