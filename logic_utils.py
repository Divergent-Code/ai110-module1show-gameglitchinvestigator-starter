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


def update_score(current_score: int, outcome: str, attempt_number: int, difficulty: str = "Normal"):
    """
    Update score based on outcome, attempt number, and difficulty multiplier.
    
    The scoring system is designed to reward efficiency (fewer attempts).
    Harder difficulties apply a higher multiplier to the base score.
    Incorrect guesses do not actively deduct points to prevent a "double penalty".
    """
    if outcome == "Win":
        # Using max() cleanly enforces the 10-point minimum floor before multipliers
        base_points = max(10, 100 - 10 * attempt_number)
        
        # Apply difficulty multiplier
        multipliers = {
            "Easy": 1.0,
            "Normal": 2.0,
            "Hard": 5.0,
            "I'm Feeling Lucky": 10.0
        }
        multiplier = multipliers.get(difficulty, 1.0)
        
        return current_score + int(base_points * multiplier)

    return current_score


# ---------------------------------------------------------------
# High Score Persistence (Agent-assisted feature)
#
# These two functions were designed and implemented with the help
# of Antigravity AI Agent during the Phase 3 challenge. The agent
# identified that separating persistence from the UI layer (app.py)
# makes both halves independently testable.
# ---------------------------------------------------------------

import json
import os

def load_high_scores(filepath: str) -> dict:
    """
    Load the high scores dictionary from a JSON file.

    Returns a dict shaped like: { "Easy": [90, 70, 50], "Normal": [...], ... }
    Returns an empty dict if the file doesn't exist or is corrupt,
    so callers never have to handle file I/O errors themselves.
    """
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Corrupt or unreadable file — start fresh rather than crash
        return {}


def save_high_score(filepath: str, difficulty: str, score: int) -> list:
    """
    Insert 'score' into the leaderboard for 'difficulty', keep the top 5,
    then persist the updated data back to the JSON file.

    Returns the updated list of scores for that difficulty so callers
    can display feedback immediately without re-reading the file.
    """
    scores = load_high_scores(filepath)

    # Get (or create) the bucket for this difficulty level
    bucket = scores.get(difficulty, [])
    bucket.append(score)

    # Sort descending and keep only the top 5 — simple but effective
    bucket = sorted(bucket, reverse=True)[:5]
    scores[difficulty] = bucket

    with open(filepath, "w") as f:
        json.dump(scores, f, indent=2)

    return bucket