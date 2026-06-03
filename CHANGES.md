# Improvements & Code Changes - Hangman_PY

This document outlines the security, architectural, and gameplay improvements applied to the Hangman_PY project. The codebase has been fully refactored from a single monolithic file into a clean modular structure, with optimized queries, structured AI integration, user authentication, and interactive hint/difficulty settings.

---

## File Changes & Structure

The codebase is now structured as follows:
*   [Hangman.py](file:///d:/Projects/Hangman_PY/Hangman.py): Application entry point and initialization.
*   [models.py](file:///d:/Projects/Hangman_PY/models.py): SQLAlchemy models (`User`, `Word`) and password helper logic.
*   [ai_services.py](file:///d:/Projects/Hangman_PY/ai_services.py): Client configuration for Google GenAI, structured outputs, and hint generation.
*   [routes.py](file:///d:/Projects/Hangman_PY/routes.py): Game routes, user authentication, difficulty-mistake mapping, AI hint penalty execution, and async generation handlers.
*   [index.html](file:///d:/Projects/Hangman_PY/templates/index.html): HTML front-end rendering authentication status, game boards, modals, hint boxes, and client-side JavaScript polling.
*   [.env](file:///d:/Projects/Hangman_PY/.env): Environment secrets.

---

## Technical Details of Applied Improvements

### 1. Security & Configuration
*   **Secure Secret Key**: Lifted the hardcoded secret key out of `Hangman.py` and placed it in `.env` as `FLASK_SECRET_KEY` so session data is cryptographically secure and credentials are kept out of version control.
*   **Safe Error Handling**: Refactored the route error outputs. If the GenAI client throws an API error, it is caught in the background thread and returned as a user-friendly message through the polling interface, avoiding raw stack trace exposure.

### 2. Architecture & Code Maintainability
*   **Modular Architecture**: Isolated the data definitions, AI connectors, and route handlers into separate files. This increases readability and ensures future changes to the models or AI APIs will not disrupt the application entry point.
*   **Database Query Optimization (Count & Offset)**: Replaced the resource-intensive `Db.func.random()` queries with a two-step Count & Offset fetch. It now gets the count of words matching the category, selects a random index, and uses `.offset(random_idx).first()` to retrieve the record, which runs in $O(1)$ time via database indexes.

### 3. AI Integration Reliability
*   **Structured Output Parsing**: Instead of parsing standard markdown/JSON text streams manually, the Gemini API is now configured with the `google-genai` SDK's `types.GenerateContentConfig` specifying `response_mime_type="application/json"` and passing a Pydantic `WordList` model. This guarantees that Gemini returns a schema-conforming JSON object `{"words": [...]}`.
*   **Asynchronous AI Generation**: Large category generation requests are now handled inside a `threading.Thread` in `routes.py`, preventing Flask worker blocking. The frontend intercepts form submissions, shows a loading page, and polls `/generate-status/<category>` using JavaScript `setInterval` until completion, ensuring seamless UI responsiveness.

### 4. Gameplay Features & Expansions
*   **User Authentication**: Implemented user registry, sign-in, and sign-out routes using hashed passwords via Werkzeug. Once logged in, the user's maximum winning streak, total wins, and total games are persisted directly to the SQL database.
*   **Difficulty Settings**: Added support for Easy, Medium, and Hard difficulty selection.
    *   **Easy**: 10 mistakes allowed, selects short words (4-7 letters).
    *   **Medium**: 8 mistakes allowed, selects medium words (8-10 letters).
    *   **Hard**: 6 mistakes allowed, selects long words (11-20 letters).
*   **AI Hint System**: Added a hint mechanism that queries Gemini for a cryptic, semantic clue for the active hidden word. To prevent abuse, getting a hint penalizes the player by increasing their mistake count by 1.
