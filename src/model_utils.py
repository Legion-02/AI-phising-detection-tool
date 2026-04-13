from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / 'models' / 'phishing_model.pkl'
DATA_PATH = ROOT_DIR / 'data' / 'raw' / 'phishing_emails.csv'
RESULTS_DIR = ROOT_DIR / 'results'


def save_artifacts(model: Any, vectorizer: Any, path: Path = MODEL_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as f:
        pickle.dump((model, vectorizer), f)


def load_artifacts(path: Path = MODEL_PATH) -> Tuple[Any, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f'Model file not found at {path}. Run `python src/train_model.py` first.'
        )
    with path.open('rb') as f:
        return pickle.load(f)
