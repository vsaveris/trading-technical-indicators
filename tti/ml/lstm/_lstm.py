"""
PyTorch implementation of an LSTM classifier for BUY/SELL/HOLD signals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

from tti.ml._model import BaseModel
from tti.ml.lstm._training_data import ID_TO_LABEL, LABEL_TO_ID


class _NumpyDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = X
        self.y = y

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int):
        # Copy to ensure tensors are writable even when backing arrays are mmap/read-only.
        x = np.array(self.X[idx], copy=True)
        y = np.array(self.y[idx], copy=True)
        return torch.from_numpy(x).float(), torch.tensor(y, dtype=torch.long)


class _LSTMClassifier(nn.Module):
    def __init__(
        self, input_size: int, hidden_size: int = 64, num_layers: int = 2, dropout: float = 0.1
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.fc = nn.Linear(hidden_size, len(LABEL_TO_ID))

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # last time step
        logits = self.fc(out)
        return logits


class LSTMModel(BaseModel):
    def __init__(
        self,
        input_size: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.1,
        lr: float = 1e-3,
        device: Optional[str] = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = _LSTMClassifier(input_size, hidden_size, num_layers, dropout).to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        if self.device == "cuda":
            torch.backends.cudnn.benchmark = True

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int = 5,
        batch_size: int = 64,
        show_progress: bool = True,
        num_workers: Optional[int] = None,
        pin_memory: Optional[bool] = None,
        non_blocking: Optional[bool] = None,
        checkpoint_dir: Optional[Path] = None,
        checkpoint_prefix: str = "epoch",
        checkpoint_every: int = 1,
        **kwargs,
    ) -> Dict[str, Any]:
        effective_workers = (
            num_workers if num_workers is not None else (4 if self.device == "cuda" else 0)
        )
        effective_pin = pin_memory if pin_memory is not None else (self.device == "cuda")
        effective_nb = non_blocking if non_blocking is not None else (self.device == "cuda")

        print(
            f"[LSTMModel] Training on {X_train.shape[0]} sequences with batch_size={batch_size}, "
            f"epochs={epochs}, device={self.device}, workers={effective_workers}, pin_memory={effective_pin}"
        )
        dataset = _NumpyDataset(X_train, y_train)
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=effective_workers,
            pin_memory=effective_pin,
        )

        history = {"loss": []}
        self.model.train()
        for epoch in range(epochs):
            epoch_loss = 0.0
            iterator = loader
            if show_progress and tqdm is not None:
                iterator = tqdm(loader, desc=f"Epoch {epoch+1}/{epochs}", leave=False)
            for batch_X, batch_y in iterator:
                batch_X = batch_X.to(self.device, non_blocking=effective_nb)
                batch_y = batch_y.to(self.device, non_blocking=effective_nb)

                self.optimizer.zero_grad()
                logits = self.model(batch_X)
                loss = self.criterion(logits, batch_y)
                loss.backward()
                self.optimizer.step()
                epoch_loss += loss.item() * batch_X.size(0)
            history["loss"].append(epoch_loss / len(dataset))
            print(f"[LSTMModel] Epoch loss: {history['loss'][-1]:.4f}")
            if checkpoint_dir and (epoch + 1) % checkpoint_every == 0:
                checkpoint_dir = Path(checkpoint_dir)
                checkpoint_dir.mkdir(parents=True, exist_ok=True)
                ckpt_path = checkpoint_dir / f"{checkpoint_prefix}_{epoch+1}.pt"
                self.save_checkpoint(ckpt_path)
                print(f"[LSTMModel] Saved checkpoint: {ckpt_path}")
        return history

    def predict(self, X: np.ndarray, return_probs: bool = False) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            inputs = torch.tensor(X, dtype=torch.float32).to(self.device)
            logits = self.model(inputs)
            if return_probs:
                return torch.softmax(logits, dim=1).cpu().numpy()
            return torch.argmax(logits, dim=1).cpu().numpy()

    def evaluate(
        self, X: np.ndarray, y_true: np.ndarray, return_report: bool = False
    ) -> Dict[str, Any]:
        """
        Compute classification metrics on provided data.
        """
        self.model.eval()
        with torch.no_grad():
            inputs = torch.tensor(X, dtype=torch.float32).to(self.device)
            logits = self.model(inputs)
            y_pred = torch.argmax(logits, dim=1).cpu().numpy()
            logits_cpu = logits.cpu()
            y_prob = torch.softmax(logits_cpu, dim=1).numpy()

        # Cross-entropy loss on provided targets
        y_true_ids = np.asarray(y_true)
        if y_true_ids.dtype.kind in {"U", "S", "O"}:
            y_true_ids = np.vectorize(LABEL_TO_ID.get)(y_true_ids)
        y_true_tensor = torch.tensor(y_true_ids, dtype=torch.long)
        ce_loss = nn.functional.cross_entropy(logits_cpu, y_true_tensor, reduction="mean").item()

        def _to_ids(arr):
            arr = np.asarray(arr)
            if arr.dtype.kind in {"U", "S", "O"}:  # string labels
                return np.vectorize(LABEL_TO_ID.get)(arr)
            return arr.astype(int)

        y_true_ids = _to_ids(y_true_ids)
        y_pred_ids = _to_ids(y_pred)

        labels = list(LABEL_TO_ID.values())
        target_names = ["BUY", "HOLD", "SELL"]

        acc = accuracy_score(y_true_ids, y_pred_ids)
        precision, recall, f1, support = precision_recall_fscore_support(
            y_true_ids, y_pred_ids, labels=labels, zero_division=0
        )
        macro_p, macro_r, macro_f, _ = precision_recall_fscore_support(
            y_true_ids, y_pred_ids, labels=labels, average="macro", zero_division=0
        )
        cm = confusion_matrix(y_true_ids, y_pred_ids, labels=labels)

        metrics = {
            "accuracy": acc,
            "loss": ce_loss,
            "macro": {"precision": macro_p, "recall": macro_r, "f1": macro_f},
            "per_class": {
                name: {"precision": float(p), "recall": float(r), "f1": float(f), "support": int(s)}
                for name, p, r, f, s in zip(target_names, precision, recall, f1, support)
            },
            "confusion_matrix": cm.tolist(),
        }
        if return_report:
            metrics["classification_report"] = classification_report(
                y_true_ids, y_pred_ids, labels=labels, target_names=target_names, zero_division=0
            )
        return metrics

    def save_checkpoint(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"state_dict": self.model.state_dict()}, path)

    @classmethod
    def load_checkpoint(
        cls,
        path: Path,
        input_size: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.1,
        lr: float = 1e-3,
        device: Optional[str] = None,
    ) -> "LSTMModel":
        instance = cls(
            input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            lr=lr,
            device=device,
        )
        checkpoint = torch.load(Path(path), map_location=instance.device)
        instance.model.load_state_dict(checkpoint["state_dict"])
        instance.model.eval()
        return instance

    def simulate(self, X: np.ndarray, prices: np.ndarray, **kwargs) -> Tuple[float, list]:
        """
        Simple simulation: start with 1.0 units cash, act on predictions at each step.
        BUY -> go long 1 unit, SELL -> go to cash, HOLD -> keep position.
        """
        preds = self.predict(X)
        decisions = [ID_TO_LABEL[p] for p in preds]

        cash = 1.0
        position = 0.0  # number of shares held
        for pred, price in zip(decisions, prices[-len(preds) :]):
            if pred == "BUY" and position == 0:
                position = cash / price
                cash = 0.0
            elif pred == "SELL" and position > 0:
                cash = position * price
                position = 0.0
            # HOLD -> no action

        final_value = cash + position * prices[-1]
        return final_value, decisions
