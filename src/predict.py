import pickle
from preprocess import clean_text

# Load model
with open('../models/phishing_model.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

# Take input
text = input("Enter email text: ")

# Preprocess
cleaned = clean_text(text)
vec = vectorizer.transform([cleaned])

# Predict
prediction = model.predict(vec)

if prediction[0] == 1:
    print("🚨 Phishing Email Detected")
else:
    print("✅ Safe Email")
