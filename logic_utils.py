"""
logic_utils.py

This module contains the core business logic for the Game Glitch Investigator application.
By separating these functions from the Streamlit UI (app.py), the code is easier to unit test,
maintain, and debug without needing to spin up the web server.
"""

def get_range_for_difficulty(difficulty: str):
    """
    Return (low, high) inclusive range for a given difficulty.

    The range dictates the possible values for the secret number.
    Wider ranges make the game harder as there are more possibilities.
    """
    # Using a dictionary makes this mapping much easier to read and expand later
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
        "I'm Feeling Lucky": (1, 200)
    }
    # Return the requested range, defaulting to (1, 100) if not found
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)

    This function handles input validation before an attempt is consumed.
    It rejects empty inputs and decimals, providing specific error messages
    so the UI can guide the user without crashing or penalizing them.
    """
    # Guard against completely empty inputs
    if not raw:
        return False, None, "Enter a guess."

    # Prevent silent truncation of decimals (e.g., entering "3.9" and it becoming 3)
    if "." in raw:
        return False, None, "Please enter a whole number, not a decimal."
        
    try:
        value = int(raw)
        return True, value, None
    except ValueError:
        # Catches letters, symbols, or other non-numeric text
        return False, None, "That is not a number."


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    
    The message returned here acts as the 'hint' displayed to the user
    after an incorrect guess.
    """
    # Removed the TypeError fallback. We now trust that 'parse_guess' 
    # and the app state strictly provide integers.
    if guess == secret:
        return "Win", "🎯 Correct!"
    elif guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.
    
    The scoring system is designed to reward efficiency: the fewer attempts
    it takes to win, the higher the final score. Incorrect guesses do not
    actively deduct points to prevent a "double penalty".
    """
    if outcome == "Win":
        # Using max() cleanly enforces the 10-point minimum floor
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    return current_score