from logic_utils import check_guess

def test_winning_guess():
    """Verify that an exact match returns a Win outcome."""
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    """Verify that a guess higher than the secret returns a 'Too High' outcome."""
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    """Verify that a guess lower than the secret returns a 'Too Low' outcome."""
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

from logic_utils import parse_guess

def test_decimal_input():
    """Ensure that float strings are rejected since the game strictly requires integers."""
    ok, value, err = parse_guess("3.14")
    assert not ok
    assert value is None
    assert err == "Please enter a whole number, not a decimal."

def test_negative_input():
    """Verify that negative integer strings are properly parsed and accepted."""
    ok, value, err = parse_guess("-5")
    assert ok
    assert value == -5
    assert err is None

def test_large_input():
    """Ensure extremely large integers do not overflow or cause parsing errors in Python."""
    ok, value, err = parse_guess("999999999999999999999")
    assert ok
    assert value == 999999999999999999999
    assert err is None

# ---------------------------------------------------------
# Tests for High Score persistence (Agent-assisted feature)
# ---------------------------------------------------------
import os
import tempfile
from logic_utils import load_high_scores, save_high_score

def test_load_high_scores_missing_file():
    """Verify that missing files are handled gracefully by returning an empty dict."""
    result = load_high_scores("definitely_does_not_exist.json")
    assert result == {}

def test_save_high_score_adds_entry():
    """Verify that a fresh file is created and the score is stored correctly on the first save."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        path = tmp.name
    os.unlink(path)  # remove so save_high_score creates it fresh
    try:
        bucket = save_high_score(path, "Easy", 80)
        assert 80 in bucket
    finally:
        if os.path.exists(path):
            os.unlink(path)

def test_save_high_score_keeps_top_five():
    """Ensure that submitting more than 5 scores correctly crops the list to keep only the top 5."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        path = tmp.name
    os.unlink(path)
    try:
        for score in [10, 20, 30, 40, 50, 60]:
            bucket = save_high_score(path, "Normal", score)
        assert len(bucket) == 5
        assert 10 not in bucket   # lowest score should be dropped
        assert 60 in bucket        # highest score should be kept
    finally:
        if os.path.exists(path):
            os.unlink(path)

