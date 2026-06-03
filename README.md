# AI-Powered Hangman Game 🎮🧠

A modernized, web-based adaptation of the classic Hangman game. This project elevates the traditional game by integrating the **Google Gemini API** to dynamically generate custom word categories on the fly, storing them locally for replayability without consuming additional API quota.

Designed with a custom "dark graph-paper" notebook aesthetic, it features modular backend components, full user authentication, dynamic UI elements, and integrated sound feedback.

---

## ✨ Features

*   **AI Category Generation:** Input any topic (e.g., *Space Exploration*, *Mythological Creatures*, or *Types of Pasta*). The Gemini API generates a tailored, clean list of matching words on the fly.
*   **Asynchronous Background Tasks:** Category generation runs in a non-blocking background thread (`threading.Thread`) while the client-side JavaScript polls status checks every 1.5 seconds, showing a modern loading spinner without locking up the server.
*   **User Portal & Authentication:**
    *   Secure User Login and Account Creation (Register) powered by `werkzeug.security` cryptographic hashing.
    *   Session tracking (`session['user_id']`) preserved across game rounds.
    *   Tracks user stats: **Highest Streak**, **Total Wins**, and **Total Games Played**.
*   **Adjustable Difficulty Tiers:**
    *   🟢 **Easy:** 10 allowed mistakes, shorter words (4–7 characters).
    *   🟡 **Medium:** 8 allowed mistakes, medium words (8–10 characters).
    *   🔴 **Hard:** 6 allowed mistakes, long words (11–20 characters).
*   **AI-Powered Gameplay Hints:** Stuck on a word? Ask the AI for a semantic hint at the cost of **3 mistakes** (requires at least 4 remaining lives to use).
*   **Persistent SQLite / PostgreSQL Integration:** Words are stored locally using SQLAlchemy to limit API calls.
*   **Optimized Selection Queries:** Word selection uses an optimized $O(1)$ count-offset selection query instead of slow random sorting (`Db.func.random()`).
*   **Responsive Dark UI:** Interactive on-screen keyboard, inverted high-contrast Hangman status SVGs, and a styled dark selection dropdown to match the dark graph-paper aesthetic.
*   **Audio Engine:** Implements micro-interactions through dynamic sound effects for correct/wrong guesses, victories, and defeats.

---

## 🛠️ Tech Stack

*   **Backend:** Python, Flask, Flask-SQLAlchemy, python-dotenv
*   **Database:** PostgreSQL (with `pg8000` driver) or SQLite (SQLAlchemy fallback)
*   **AI Service:** Google Gemini API (`google-genai` SDK)
*   **Frontend:** HTML5, Bootstrap 5, Custom Vanilla CSS, Jinja2 Templating
*   **Automated Testing:** GitHub Actions CI pipeline (`ci.yml`) for automated syntax compilation tests.

---

## 📂 File Structure

```text
Hangman_PY/
├── .github/
│   └── workflows/
│       └── ci.yml            # CI pipeline verifying Python compilation
├── static/
│   ├── images/               # Hangman status images (hangman0.png to hangman10.png)
│   └── sounds/               # Sound assets (correct.mp3, wrong.mp3, win.mp3, lose.mp3)
├── templates/
│   └── index.html            # Core frontend UI template (Bootstrap 5 + Custom CSS)
├── .env                      # Environment configurations (API key & secrets - git-ignored)
├── .gitignore                # Git ignore rules
├── Hangman.py                # Main entry point and Flask app initializations
├── ai_services.py            # Gemini API client wrapper & Pydantic structured output models
├── models.py                 # SQLAlchemy Database models (User & Word schemas)
├── routes.py                 # Blueprint routes, gameplay logic, and authentication endpoints
├── requirements.txt          # Python library dependencies
└── README.md                 # Project documentation
```

---

## 🚀 How to Run the Project Locally

Follow these steps to configure, set up, and play the game on your local machine.

### Prerequisites

*   Python `3.10` or higher installed.
*   PostgreSQL installed (or use SQLite by configuring the database URL).
*   A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com).

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sikki-Codez/Hangman_Project-PY-.git
cd Hangman_Project-PY-
```

### Step 2: Configure the Environment (`.env`)

1. Create a file named `.env` in the root directory of the project.
2. Open the file in a text editor and add the following configuration:

```env
# Google Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Flask session security secret key
FLASK_SECRET_KEY=generate_some_secure_random_string_here

# Database URI Connection String
# PostgreSQL example:
DATABASE_URL=postgresql+pg8000://postgres:YOUR_PASSWORD@localhost:5432/Hangman
# SQLite example (uncomment to use):
# DATABASE_URL=sqlite:///hangman.db
```

*Note: If you use PostgreSQL, make sure to open pgAdmin 4 or your client and create a database named exactly `Hangman` first. SQLAlchemy will automatically create the tables inside it when you start the server.*

### Step 3: Install Dependencies

Set up a Python virtual environment to manage dependencies securely:

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Run the Application

Start the Flask development server:

```bash
python Hangman.py
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🎯 How to Play

1.  **Register / Log In:** Click the **Login / Register** button in the navbar to save your streaks, games played, and wins to the database.
2.  **Generate a Category:** Use the left panel to request a new AI category (e.g., *Cryptocurrency*, *Famous Scientists*). The generator automatically builds 100 relevant words matching your difficulty constraints.
3.  **Play Saved Categories:** Pick any category from the list in the right panel. Adjust the difficulty selector dropdown first to scale mistake limits.
4.  **Guess Letters:** Click the interactive on-screen keyboard buttons or use the keyboard to guess characters in the word.
5.  **Get AI Hints:** Click **Get AI Hint** to get a context clue. Using a hint costs **3 mistakes** and can only be used if you have at least 4 remaining mistakes to spare.
6.  **Manage Saved Data:** Clean up your database list by clicking the trash bin icon (`🗑️`) next to any saved category.
