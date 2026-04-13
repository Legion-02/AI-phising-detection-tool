from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, classification_report, confusion_matrix

from src.model_utils import DATA_PATH, RESULTS_DIR, load_artifacts
from src.preprocess import clean_text


def evaluate() -> tuple[float, str]:
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=['text', 'label']).copy()
    df['clean_text'] = df['text'].apply(clean_text)

    model, vectorizer = load_artifacts()
    X = vectorizer.transform(df['clean_text'])
    y = df['label'].astype(int)
    preds = model.predict(X)

    accuracy = accuracy_score(y, preds)
    report = classification_report(y, preds)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y, preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Safe', 'Phishing'])
    disp.plot()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'confusion_matrix.png')
    plt.close()

    plt.figure()
    plt.bar(['Accuracy'], [accuracy])
    plt.ylim(0, 1)
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'accuracy.png')
    plt.close()

    return accuracy, report


if __name__ == '__main__':
    accuracy, report = evaluate()
    print(f'Accuracy: {accuracy:.4f}')
    print(report)
    print(f'Results saved in: {RESULTS_DIR}')
