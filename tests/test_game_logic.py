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
