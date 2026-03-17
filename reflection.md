# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it was completely playable but full of frustrating logic flaws. For example, the difficulty limits were backwards; "Hard" mode gave a smaller range of numbers (1–50) than "Normal" mode (1–100). Additionally, the hints were inverted, so if my guess was too high, the game incorrectly told me to "📈 Go HIGHER!" instead of telling me to lower my guess.

---

## 2. How did you use AI as a teammate?

I used the Gemini/Antigravity AI agent as my primary coding partner to help plan features and review code logic. One highly correct suggestion the AI made was identifying an off-by-one error in the `update_score` function, pointing out that wrong guesses were unfairly double-penalizing the player. However, it also gave a misleading suggestion when building the High Score feature by trying to use the `.get()` method on a standard Python list. I verified this was incorrect when the Streamlit app crashed with an `AttributeError`, forcing me to report the traceback to the AI so we could switch to standard list indexing.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by combining manual testing in the browser with automated verification. For manual testing, I would refresh the Streamlit app, purposely enter invalid data like decimals, and verify that my new error messages appeared without consuming a player attempt. The AI was extremely helpful in designing automated tests; it pointed out that my initial `pytest` assertions were broken because `check_guess` returned a tuple, and it showed me how to rewrite them as `assert result[0] == "Win"` to properly verify the logic.

---

## 4. What did you learn about Streamlit and state?

The original app's secret number kept behaving weirdly because a glitch in the code actively converted the integer into a string on every even attempt, breaking the game's ability to compare numbers. Streamlit is unique because it completely reruns your script from top to bottom every single time you click a button or type in a box; "session state" acts like a persistent backpack so the app doesn't forget important variables during those constant reruns. I stabilized the game by completely removing the even-attempt type juggling and ensuring `st.session_state.secret` only resets when a player intentionally clicks "New Game" or changes the difficulty.

---

## 5. Looking ahead: your developer habits

One habit I will carry forward is carefully tracking where and when application state gets updated, since incrementing attempts _before_ validating input caused major bugs in this project. Next time I work with AI, I will ask it to map out the entire data flow of the application before we start fixing individual functions to avoid integration errors. Ultimately, this project taught me that AI can generate code that looks syntactically perfect but harbors deep logic flaws, proving that the human developer must always be the lead architect.
