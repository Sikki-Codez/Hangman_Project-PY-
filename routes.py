import threading
import random
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify, g, current_app
from models import Db, Word, User
from ai_services import generate_words, generate_hint

bp = Blueprint('routes', __name__)

GENERATING_CATEGORIES = set()
GENERATION_ERRORS = {}

def async_generate_task(app, category_name, word_count, min_len, max_len):
    with app.app_context():
        try:
            words = generate_words(category_name, word_count, min_len, max_len)
            valid_words = []
            for w in words:
                exists = Word.query.filter_by(TargetWord=w, Category=category_name).first()
                if not exists:
                    valid_words.append(Word(TargetWord=w, Category=category_name))
            
            if valid_words:
                Db.session.bulk_save_objects(valid_words)
                Db.session.commit()
            else:
                existing_count = Word.query.filter_by(Category=category_name).count()
                if existing_count == 0:
                    raise Exception("AI failed to generate any valid words.")
        except Exception as e:
            GENERATION_ERRORS[category_name] = str(e)
            print(f"Error in background generation: {e}")
        finally:
            GENERATING_CATEGORIES.discard(category_name)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Db.session.get(User, user_id)

@bp.route('/')
def Index():
    auth_error = session.pop('auth_error', None)
    
    if 'word' not in session:
        # Load distinct categories safely
        categories = [cat[0] for cat in Db.session.query(Word.Category).distinct().all()]
        return render_template('index.html', show_menu=True, available_categories=categories, auth_error=auth_error)

    if 'streak' not in session:
        session['streak'] = 0

    display_word = ""
    guessed = session.get('guessed', [])
    for char in session['word']:
        if char == " ":
            display_word += "&nbsp;&nbsp;"
        elif char in guessed:
            display_word += char + " "
        else:
            display_word += "_ "

    # Check winning status
    clean_word = session['word'].replace(" ", "")
    has_won = True
    for char in clean_word:
        if char not in guessed:
            has_won = False
            break

    max_mistakes = session.get('max_mistakes', 10)

    if has_won and not session.get('game_over'):
        session['win'] = True
        session['game_over'] = True
        session['last_action'] = 'win'
        if g.user:
            g.user.TotalGames += 1
            g.user.TotalWins += 1
            session['streak'] += 1
            if session['streak'] > g.user.HighestStreak:
                g.user.HighestStreak = session['streak']
            Db.session.commit()
        else:
            session['streak'] = session.get('streak', 0) + 1
        session.modified = True
    elif session['mistakes'] >= max_mistakes and not session.get('game_over'):
        session['win'] = False
        session['game_over'] = True
        session['last_action'] = 'lose'
        if g.user:
            g.user.TotalGames += 1
            session['streak'] = 0
            Db.session.commit()
        else:
            session['streak'] = 0
        session.modified = True

    sound_to_play = session.pop('last_action', None)

    return render_template('index.html',
                           show_menu=False,
                           category=session.get('category'),
                           streak=session['streak'],
                           display=display_word,
                           mistakes=session['mistakes'],
                           max_mistakes=max_mistakes,
                           difficulty=session.get('difficulty', 'easy'),
                           game_over=session.get('game_over'),
                           win=session.get('win'),
                           secret_word=session['word'],
                           guessed_letters=session.get('guessed', []),
                           sound_to_play=sound_to_play,
                           hint=session.get('hint'),
                           auth_error=auth_error)

@bp.route('/register', methods=['POST'])
def Register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        session['auth_error'] = "Username and password are required."
        return redirect(url_for('routes.Index'))
        
    existing = User.query.filter_by(Username=username).first()
    if existing:
        session['auth_error'] = "Username already exists."
        return redirect(url_for('routes.Index'))
        
    new_user = User(Username=username)
    new_user.set_password(password)
    Db.session.add(new_user)
    Db.session.commit()
    
    session['user_id'] = new_user.Id
    session['streak'] = 0
    session.pop('auth_error', None)
    return redirect(url_for('routes.Index'))

@bp.route('/login', methods=['POST'])
def Login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    user = User.query.filter_by(Username=username).first()
    if not user or not user.check_password(password):
        session['auth_error'] = "Invalid username or password."
        return redirect(url_for('routes.Index'))
        
    session['user_id'] = user.Id
    session['streak'] = user.HighestStreak
    session.pop('auth_error', None)
    return redirect(url_for('routes.Index'))

@bp.route('/logout')
def Logout():
    session.clear()
    return redirect(url_for('routes.Index'))

@bp.route('/generate', methods=['POST'])
def Generate():
    category_name = request.form.get('category_name', '').strip().title()
    word_count = int(request.form.get('word_count') or 100)
    difficulty = request.form.get('difficulty', 'easy')
    
    if difficulty == 'easy':
        min_len = 4
        max_len = 7
        max_mistakes = 10
    elif difficulty == 'medium':
        min_len = 8
        max_len = 10
        max_mistakes = 8
    else:  # hard
        min_len = 11
        max_len = 20
        max_mistakes = 6
        
    session['difficulty'] = difficulty
    session['max_mistakes'] = max_mistakes
    
    if not category_name:
        return jsonify({"status": "failed", "error": "Category name is required."}), 400
        
    # Check if category already exists
    existing = Word.query.filter_by(Category=category_name).first()
    if existing:
        return jsonify({"status": "completed", "category": category_name})
        
    if category_name in GENERATING_CATEGORIES:
        return jsonify({"status": "processing", "category": category_name})
        
    # Launch async generation thread
    GENERATING_CATEGORIES.add(category_name)
    GENERATION_ERRORS.pop(category_name, None)
    
    app = current_app._get_current_object()
    thread = threading.Thread(target=async_generate_task, args=(app, category_name, word_count, min_len, max_len))
    thread.start()
    
    return jsonify({"status": "processing", "category": category_name})

@bp.route('/generate-status/<category_name>')
def GenerateStatus(category_name):
    category_name = category_name.title()
    # Check count in DB
    count = Word.query.filter_by(Category=category_name).count()
    if count > 0:
        return jsonify({"status": "completed"})
        
    if category_name in GENERATING_CATEGORIES:
        return jsonify({"status": "processing"})
        
    error = GENERATION_ERRORS.get(category_name)
    if error:
        return jsonify({"status": "failed", "error": error})
        
    return jsonify({"status": "not_started"})

@bp.route('/start', methods=['POST'])
def Start():
    selected_category = request.form.get('category')
    difficulty = request.form.get('difficulty', 'easy')
    
    if difficulty == 'easy':
        max_mistakes = 10
    elif difficulty == 'medium':
        max_mistakes = 8
    else:  # hard
        max_mistakes = 6
        
    session['difficulty'] = difficulty
    session['max_mistakes'] = max_mistakes
    
    if selected_category:
        return start_game_for_category(selected_category)
        
    return redirect(url_for('routes.Index'))

@bp.route('/start-game/<category_name>')
def StartGame(category_name):
    return start_game_for_category(category_name)

def start_game_for_category(category_name):
    # Optimize query (Solution 1: Count & Offset)
    count = Word.query.filter_by(Category=category_name).count()
    if count == 0:
        return redirect(url_for('routes.Index'))
        
    random_idx = random.randint(0, count - 1)
    random_word = Word.query.filter_by(Category=category_name).offset(random_idx).first()
    
    if random_word:
        session['word'] = random_word.TargetWord.lower()
        session['category'] = category_name
        session['guessed'] = []
        session['mistakes'] = 0
        session['game_over'] = False
        session['win'] = False
        session.pop('hint', None)
        if 'max_mistakes' not in session:
            session['max_mistakes'] = 10
            session['difficulty'] = 'easy'
            
    return redirect(url_for('routes.Index'))

@bp.route('/guess', methods=['POST'])
def Guess():
    if not session.get('game_over'):
        guessed_letter = request.form.get('letter', '').lower()
        if guessed_letter and guessed_letter.isalpha() and guessed_letter not in session.get('guessed', []):
            if 'guessed' not in session:
                session['guessed'] = []
            session['guessed'].append(guessed_letter)
            
            if guessed_letter in session['word']:
                session['last_action'] = 'correct'
            else:
                session['mistakes'] += 1
                session['last_action'] = 'wrong'
            session.modified = True
    return redirect(url_for('routes.Index'))

@bp.route('/hint', methods=['POST'])
def Hint():
    if not session.get('game_over') and 'word' in session:
        max_mistakes = session.get('max_mistakes', 10)
        # Deduct 3 lives for using a hint; must have at least 4 mistakes left to use it safely
        if session.get('mistakes', 0) <= max_mistakes - 4:
            clue = generate_hint(session['word'], session.get('guessed', []))
            session['hint'] = clue
            session['mistakes'] = session.get('mistakes', 0) + 3
            session['last_action'] = 'wrong'  # Trigger correction sound/feedback
            session.modified = True
    return redirect(url_for('routes.Index'))

@bp.route('/delete_category/<category_name>', methods=['POST'])
def DeleteCategory(category_name):
    Word.query.filter_by(Category=category_name).delete()
    Db.session.commit()
    return redirect(url_for('routes.Index'))

@bp.route('/reset')
def Reset():
    user_id = session.get('user_id')
    current_streak = session.get('streak', 0)
    # Save key stats
    difficulty = session.get('difficulty', 'easy')
    max_mistakes = session.get('max_mistakes', 10)
    session.clear()
    if user_id is not None:
        session['user_id'] = user_id
    session['streak'] = current_streak
    session['difficulty'] = difficulty
    session['max_mistakes'] = max_mistakes
    return redirect(url_for('routes.Index'))
