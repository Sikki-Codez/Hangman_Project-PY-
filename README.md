# AI-Powered Hangman Game 🎮🧠

A modernized, web-based adaptation of the classic Hangman game. This project elevates the traditional game by integrating the **Google Gemini API** to dynamically generate custom word categories on the fly, storing them locally via **PostgreSQL** for future replayability without consuming additional API quota.

Designed with a custom "dark graph-paper" notebook aesthetic, it features full session management, dynamic UI updates, and integrated sound effects, showcasing a complete full-stack integration.

## ✨ Features
* **AI Category Generation:** Type any topic (e.g., "Space Exploration" or "Types of Pasta") and the Gemini 2.5 Flash model will instantly generate a curated list of words matching your specific length constraints.
* **Persistent Local Database:** All AI-generated categories are cleaned, validated, and saved to a local PostgreSQL database.
* **Smart UI/UX:** * Custom dark mode notebook aesthetic with a CSS grid background.
  * Interactive on-screen keyboard that visually disables guessed letters.
  * Dynamic, high-contrast Hangman graphics that invert cleanly on dark backgrounds.
  * Loading spinners for asynchronous AI background tasks.
* **Audio Feedback:** Integrated sound effects for correct guesses, wrong guesses, victories, and game overs.
* **Automated CI/CD:** Includes a GitHub Actions pipeline (`ci.yml`) to automatically verify Python syntax and compilation on every push.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-Session
* **Database:** PostgreSQL (pgAdmin 4), SQLAlchemy, pg8000
* **AI Integration:** Google GenAI SDK (`gemini-2.5-flash`)
* **Frontend:** HTML5, Bootstrap 5, Custom CSS, Jinja2 Templating

## 📂 Repository Structure
```text
├── .github/workflows/
│   └── ci.yml            # GitHub Actions automated testing pipeline
├── static/               
│   ├── images/           # hangman0.png through hangman10.png
│   └── sounds/           # correct.mp3, wrong.mp3, win.mp3, lose.mp3
├── templates/            
│   └── index.html        # Main Jinja/HTML application layout
├── .gitignore            # Ignores local environments and secret API keys
├── Hangman.py            # Core Flask application, DB schema, and API logic
└── requirements.txt      # Python dependencies and package versions

```

# 🚀 How to Run This Project Locally

Follow these steps to set up the development environment and play the game on your own machine.

## Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.10 or higher
* PostgreSQL (and pgAdmin 4 for easy local database management)
* A free Google Gemini API Key (You can claim one at Google AI Studio)

## Step 1: Clone the Repository

Open your terminal or command prompt and download the code:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
```

## Step 2: Set Up the Database

This application requires a local database to save the AI-generated categories.

1. Open pgAdmin 4 (or your preferred PostgreSQL client).
2. Create a brand new, empty database and name it exactly: `Hangman`

> **Note:** You do not need to manually create any tables. SQLAlchemy will automatically build the necessary data tables the first time you run the application.

## Step 3: Configure Environment Variables

Because API keys are private, they are intentionally excluded from this repository. You must create your own configuration file.

1. In the root folder of the project (right next to `Hangman.py`), create a new file named exactly `.env` (do not forget the leading dot).
2. Open `.env` in any text editor and add your Gemini API key and your local database credentials:

```env
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=postgresql+pg8000://postgres:YOUR_PGADMIN_PASSWORD@localhost:5432/Hangman
```

## Step 4: Install Dependencies

It is highly recommended to use a virtual environment to avoid package conflicts. Run the following commands in your terminal:


**For Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Launch the Game

With the database ready and packages installed, start the local Flask development server:

**For Windows:**
```bash
python Hangman.py
```

Finally, open your web browser and navigate to http://127.0.0.1:5000 to start playing!


## HOW TO PLAY: 

* Choose a Category: Select a previously saved category from the right panel on the main menu, or use the AI generator on the left to create a brand new, highly specific category.
* Make Guesses: Click the on-screen keyboard to guess letters.
* Survive: You are allowed up to 10 total mistakes before the Hangman is fully drawn and the game ends.
* Manage Data: Click the 🗑️ icon next to any saved category on the main menu to permanently delete those words from your local database.
