from __future__ import annotations

import argparse

from src.model_utils import load_artifacts
from src.preprocess import clean_text, extract_reasons


def predict_text(text: str) -> dict:
    model, vectorizer = load_artifacts()
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    prediction = int(model.predict(vec)[0])
    if hasattr(model, 'predict_proba'):
        proba = float(model.predict_proba(vec)[0][prediction])
    else:
        proba = 0.0
    return {
        'label': 'Phishing' if prediction == 1 else 'Safe',
        'prediction': prediction,
        'confidence': proba,
        'reasons': extract_reasons(text),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict whether a message is phishing.')
    parser.add_argument('--text', required=True, help='Email or message text to classify.')
    args = parser.parse_args()
    result = predict_text(args.text)
    print(f"Prediction: {result['label']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print('Reasons:')
    for item in result['reasons']:
        print(f'- {item}')
