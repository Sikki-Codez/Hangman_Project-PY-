# AI-Powered Hangman Web App 🎮🧠

A modernized, web-based adaptation of the classic Hangman game built with Python and Flask. This project elevates the traditional game by integrating the **Google Gemini API** to dynamically generate custom word categories on the fly, storing them locally via **PostgreSQL** for future replayability. 

Designed with a custom "dark graph-paper" aesthetic, it features full session management, dynamic UI updates, and integrated sound effects.

## ✨ Features
* **AI Category Generation:** Type any topic (e.g., "Space Exploration" or "Types of Pasta") and the Gemini 2.5 Flash model will instantly generate a curated list of words matching your specific length constraints.
* **Persistent Local Database:** All AI-generated categories are cleaned, validated, and saved to a local PostgreSQL database so you can replay your custom categories without using up API quota.
* **Smart UI/UX:** * Dark mode notebook aesthetic with a custom CSS grid.
  * Interactive on-screen keyboard that disables guessed letters.
  * Dynamic, high-contrast Hangman graphics.
  * Loading spinners for asynchronous AI background tasks.
* **Audio Feedback:** Integrated sound effects for correct guesses, wrong guesses, victories, and game overs.
* **Automated CI/CD:** Includes a GitHub Actions pipeline (`ci.yml`) to automatically verify Python syntax and compilation on every push.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-Session
* **Database:** PostgreSQL (pgAdmin), SQLAlchemy, pg8000
* **AI Integration:** Google GenAI SDK (`gemini-2.5-flash`)
* **Frontend:** HTML5, Bootstrap 5, Custom CSS, Jinja2 Templating

## 📂 Project Structure
```text
HMW/
├── .github/workflows/
│   └── ci.yml            # GitHub Actions automated testing
├── static/               
│   ├── images/           # hangman0.png through hangman10.png
│   └── sounds/           # correct.mp3, wrong.mp3, win.mp3, lose.mp3
├── templates/            
│   └── index.html        # Main Jinja/HTML layout
├── .env                  # Secret API keys (Not tracked by Git)
├── .gitignore            
├── Hangman.py            # Core Flask application and API logic
└── requirements.txt      # Python dependencies
