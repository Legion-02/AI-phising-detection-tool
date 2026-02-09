import pandas as pd
import pickle
from sklearn.metrics import classification_report
from preprocess import clean_text

df = pd.read_csv('data/raw/phishing_emails.csv')
df['clean_text'] = df['text'].apply(clean_text)

with open('models/phishing_model.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

X = vectorizer.transform(df['clean_text'])
y = df['label']

preds = model.predict(X)
print(classification_report(y, preds))