import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import clean_text

os.makedirs("models", exist_ok=True)

df = pd.read_csv('data/raw/phishing_emails.csv')
df['clean_text'] = df['text'].apply(clean_text)

X = df['clean_text']
y = df['label']

vectorizer = TfidfVectorizer(max_features=1000)
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

with open('models/phishing_model.pkl', 'wb') as f:
    pickle.dump((model, vectorizer), f)

print("Model trained and saved successfully")