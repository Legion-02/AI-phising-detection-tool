from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

from src.preprocess import clean_text, extract_reasons  # noqa: E402


def test_clean_text_removes_url_and_keeps_words():
    result = clean_text('Visit https://example.com now to verify your Account!')
    assert 'url' in result
    assert 'account' in result


def test_extract_reasons_finds_urgency():
    reasons = extract_reasons('Urgent! Reset your password immediately.')
    assert any('urgency' in r.lower() or 'password' in r.lower() for r in reasons)
