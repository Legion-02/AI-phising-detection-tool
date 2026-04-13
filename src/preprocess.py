from __future__ import annotations

import re
from functools import lru_cache

try:
    from nltk.corpus import stopwords as nltk_stopwords
except Exception:
    nltk_stopwords = None


FALLBACK_STOPWORDS = {
    'a','an','the','and','or','but','if','while','with','to','from','for','of','on','in','at','by','is','are','was','were','be','been','being',
    'this','that','these','those','it','its','as','into','about','than','then','so','such','you','your','yours','me','my','we','our','ours',
    'he','she','they','them','their','theirs','i','am','do','does','did','done','have','has','had','not','no','yes','can','could','will','would',
    'should','may','might','must','all','any','some','more','most','other','another','few','many','very','here','there','now','today','tomorrow'
}


@lru_cache(maxsize=1)
def _english_stopwords() -> set[str]:
    if nltk_stopwords is not None:
        try:
            return set(nltk_stopwords.words('english'))
        except LookupError:
            pass
    return FALLBACK_STOPWORDS


def clean_text(text: str | None) -> str:
    """Normalize email text for ML inference/training."""
    text = str(text or '').lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' url ', text)
    text = re.sub(r'\S+@\S+', ' email ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = [w for w in text.split() if w not in _english_stopwords() and len(w) > 1]
    return ' '.join(words)


SUSPICIOUS_KEYWORDS = {
    'urgent', 'verify', 'account', 'suspended', 'reset', 'password', 'click', 'bank',
    'invoice', 'payment', 'gift', 'winner', 'lottery', 'confirm', 'security', 'limited',
    'login', 'credential', 'update', 'immediately', 'otp', 'alert'
}


def extract_reasons(text: str | None) -> list[str]:
    """Return human-readable clues for GUI display."""
    raw = str(text or '')
    lowered = raw.lower()
    reasons: list[str] = []

    found_keywords = sorted({kw for kw in SUSPICIOUS_KEYWORDS if kw in lowered})
    if found_keywords:
        reasons.append('Suspicious keywords: ' + ', '.join(found_keywords[:6]))

    if re.search(r'https?://|www\.', lowered):
        reasons.append('Contains a URL or web link.')

    if re.search(r'\b(click|verify|confirm|reset|login|act now)\b', lowered):
        reasons.append('Uses action-oriented language often seen in phishing messages.')

    if re.search(r'\b(urgent|immediately|asap|limited time|final warning)\b', lowered):
        reasons.append('Creates urgency or pressure.')

    if re.search(r'\b(password|otp|credential|bank|account)\b', lowered):
        reasons.append('Requests sensitive account or security information.')

    if not reasons:
        reasons.append('No obvious phishing indicators were detected from the entered text.')

    return reasons
