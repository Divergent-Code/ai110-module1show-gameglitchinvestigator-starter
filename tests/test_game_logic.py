from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

from logic_utils import parse_guess

def test_decimal_input():
    # Test decimal numbers
    ok, value, err = parse_guess("3.14")
    assert not ok
    assert value is None
    assert err == "Please enter a whole number, not a decimal."

def test_negative_input():
    # Test negative numbers
    ok, value, err = parse_guess("-5")
    assert ok
    assert value == -5
    assert err is None

def test_large_input():
    # Test extremely large values
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
    # A non-existent file path should return an empty dict, not crash
    result = load_high_scores("definitely_does_not_exist.json")
    assert result == {}

def test_save_high_score_adds_entry():
    # A fresh file should be created and the score stored correctly
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
    # After submitting 6 scores, only the top 5 should be retained
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

