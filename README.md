# AI-Based Phishing Detection System with Tkinter GUI

A desktop phishing detection project that classifies email or message text as **Phishing** or **Safe** using NLP and machine learning. This version includes a **Tkinter GUI**, so it works like a local desktop tool similar to your WRM project.

## Features  
- Tkinter desktop interface  
- Paste email or message content and analyze instantly  
- Prediction label with confidence score  
- Human-readable reason hints for the result  
- Session history inside the GUI  
- Separate training, prediction, and evaluation scripts  
- Confusion matrix and accuracy chart generation  

## Project Structure
```text
AI-phising-detection-tool/
├── data/
│   └── raw/
│       └── phishing_emails.csv
├── models/
│   └── phishing_model.pkl
├── results/
│   ├── accuracy.png
│   └── confusion_matrix.png
├── src/
│   ├── evaluate_model.py
│   ├── model_utils.py
│   ├── predict.py
│   ├── preprocess.py
│   └── train_model.py
├── tests/
│   └── test_preprocess_and_predict.py
├── gui.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation
```bash
python -m venv venv
```

### Windows
```bash
venv\Scripts\activate
pip install -r requirements.txt
python src/train_model.py
python gui.py
```

### Linux / Kali
```bash
source venv/bin/activate
pip install -r requirements.txt
python src/train_model.py
python gui.py
```

## CLI Prediction Example
```bash
python src/predict.py --text "Urgent: click this link to reset your password now"
```

## Evaluate the Model
```bash
python src/evaluate_model.py
```

## Packaging as EXE
After testing the GUI, you can convert it into an executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed gui.py
```

The executable will be created inside the `dist/` folder.

## Notes
- Run `python src/train_model.py` before opening the GUI if the model file does not exist yet.
- `venv/`, `__pycache__/`, and `.pytest_cache/` should not be uploaded to GitHub.

## Author
Anush - Cybersecurity Enthusiast
