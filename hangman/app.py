import os
from re import A

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology #lookup, usd, apology
from hangman import chooseWord, isWordGuessed, loadWords, getGuessedWord, getAvailableLetters

wordList = loadWords()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}   

@app.route("/leaderboard")
def leaderboard():
    results = db.execute("SELECT users.username, scores.score FROM scores INNER JOIN users ON scores.person_id = users.id ORDER BY score DESC")
    res = dict()
    for result in results:
        if result['username'] not in res:
            res[result['username']] = result['score']
        elif result['score'] > res[result['username']]:
            res[result['username']] = result['score'] 
    return render_template("leaderboard.html", res=res)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        secretWord = chooseWord(wordList)
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        guessedWord = ("_ ") * len(secretWord)
        if request.args.get('button') == 'continue':
            score = db.execute("SELECT score FROM hangman WHERE person_id = ?", session['user_id'])
            score = score[0]['score']
            
        else:
            score = 0
        db.execute("UPDATE hangman SET score = ? WHERE person_id = ?", score, session['user_id'])
        db.execute("UPDATE hangman SET secretWord = ? WHERE person_id = ?", secretWord, session['user_id'])
        db.execute("UPDATE hangman SET guesses = ? WHERE person_id = ?", 8, session['user_id'])
        db.execute("UPDATE hangman SET lettersGuessed = ? WHERE person_id = ?", "", session['user_id'])
        db.execute("UPDATE hangman SET guessedWord = ? WHERE person_id = ?", "", session['user_id'])
        db.execute("UPDATE hangman SET availableLetters = ? WHERE person_id = ?", "", session['user_id'])
        return render_template("index.html", available_letters=alphabet, guesses=8, score=score, guessedWord=guessedWord)
    
    elif request.method == "POST":
        secretWord = db.execute("SELECT secretWord FROM hangman WHERE person_id = ?", session['user_id'])
        secretWord = secretWord[0]['secretWord']
        guesses = db.execute("SELECT guesses FROM hangman WHERE person_id = ?", session['user_id'])
        guesses = guesses[0]['guesses']
        score = db.execute("SELECT score FROM hangman WHERE person_id = ?", session['user_id'])
        score = score[0]['score']
        letter = request.form.get("button")
        if letter in secretWord:
            letter_score = secretWord.count(letter)
            letter_score *= int(SCRABBLE_LETTER_VALUES[letter])
            score += letter_score
            db.execute("UPDATE hangman SET score = ? WHERE person_id = ?", score, session['user_id'])
            print(score)
        if letter not in secretWord:
            guesses -= 1
            db.execute("UPDATE hangman SET guesses = ? WHERE person_id = ?", guesses, session['user_id'])
        if guesses == 0:
            db.execute("INSERT INTO scores (person_id, score) VALUES(?, ?)", session['user_id'], score)
            return render_template('lost.html', score=score, secretWord=secretWord)
        lettersGuessed = db.execute("SELECT lettersGuessed FROM hangman WHERE person_id = ?", session['user_id'])
        lettersGuessed = lettersGuessed[0]['lettersGuessed']
        print(lettersGuessed)
        newLettersGuessed = lettersGuessed + letter
        guessedWord = getGuessedWord(secretWord, newLettersGuessed)
        if isWordGuessed(secretWord, newLettersGuessed):
            score += 50
            db.execute("INSERT INTO scores (person_id, score) VALUES(?, ?)", session['user_id'], score)
            db.execute("UPDATE hangman SET score = ? WHERE person_id = ?", score, session['user_id'])
            return render_template('victory.html', score=score, secretWord=secretWord)
        available_letters = getAvailableLetters(newLettersGuessed)
        db.execute("UPDATE hangman SET lettersGuessed = ? WHERE person_id = ?", newLettersGuessed, session['user_id'])
        print(letter)
        return render_template("index.html", available_letters=available_letters, guesses=guesses, guessedWord=guessedWord, score=score)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return 


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return #apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    
    # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

    # Ensure username doesn't already exist
        user_name = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(user_name) != 0:
            return apology("user already exists", 403)

    # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

    # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

    # Ensure password and password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation don't match", 403)
        
    # Register for an account
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        user_id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        user_id = user_id[0]['id']
        db.execute("INSERT INTO hangman (person_id) VALUES(?)", user_id)
        return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return #apology("TODO")
