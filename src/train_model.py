from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.model_utils import DATA_PATH, MODEL_PATH, save_artifacts
from src.preprocess import clean_text


def train() -> tuple[float, int]:
    df = pd.read_csv(DATA_PATH)
    required_columns = {'text', 'label'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f'Dataset must contain columns: {required_columns}')

    df = df.dropna(subset=['text', 'label']).copy()
    df['clean_text'] = df['text'].apply(clean_text)

    X = df['clean_text']
    y = df['label'].astype(int)

    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vec,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if y.nunique() > 1 else None,
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    save_artifacts(model, vectorizer, MODEL_PATH)
    return accuracy, len(df)


if __name__ == '__main__':
    accuracy, rows = train()
    print(f'Model trained successfully on {rows} rows.')
    print(f'Model saved to: {MODEL_PATH}')
    print(f'Validation accuracy: {accuracy:.4f}')
