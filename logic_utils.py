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
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    if difficulty == "I'm Feeling Lucky":
        # Uses the Hard range for maximum difficulty on a single attempt
        return 1, 200
    return 1, 100


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

    try:
        # Prevent silent truncation of decimals (e.g., entering "3.9" and it becoming 3)
        if "." in raw:
            return False, None, "Please enter a whole number, not a decimal."
        value = int(raw)
    except ValueError:
        # Catches letters, symbols, or other non-numeric text
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    
    The message returned here acts as the 'hint' displayed to the user
    after an incorrect guess.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # Standard numeric comparison
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # Fallback block: If the types somehow mismatch (e.g., string vs int),
        # force them into a common format (strings, then ints) to compare safely.
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if int(g) > int(secret):
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.
    
    The scoring system is designed to reward efficiency: the fewer attempts
    it takes to win, the higher the final score.
    """
    if outcome == "Win":
        # Base win score is 100, subtracting 10 points for every attempt made.
        points = 100 - 10 * attempt_number
        
        # Implement a score floor: no matter how many attempts it took,
        # winning always grants at least 10 points.
        if points < 10:
            points = 10
        return current_score + points

    # Incorrect guesses do not actively deduct points. This prevents a "double penalty"
    # since the attempt_number multiplier above already reduces the potential win score.
    return current_score
