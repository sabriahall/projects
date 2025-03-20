import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from security.encryption import encrypt_data, decrypt_data

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "YOUR_SECRET_KEY_HERE"  # Replace with your secret key
Session(app)

# Database helper function
def get_db():
    conn = sqlite3.connect("habit_tracker.db")
    conn.row_factory = sqlite3.Row  # Enables dict-like access to rows
    return conn

# Custom login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in to continue.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    """Display all habits for the logged-in user (decrypted)."""
    db = get_db()
    user_id = session["user_id"]
    rows = db.execute("SELECT id, habit, date FROM habits WHERE user_id = ?", (user_id,)).fetchall()
    db.close()
    habits = []
    for row in rows:
        # Decrypt habit text before display
        habits.append({
            "id": row["id"],
            "habit": decrypt_data(row["habit"]),
            "date": row["date"]
        })
    return render_template("index.html", habits=habits)

@app.route("/add_habit", methods=["GET", "POST"])
@login_required
def add_habit():
    """Add a new habit (encrypted) for the logged-in user."""
    if request.method == "POST":
        habit_text = request.form.get("habit")
        if not habit_text:
            return render_template("apology.html", message="Must provide a habit description.")

        user_id = session["user_id"]
        # Encrypt the habit text before storing it in the database
        encrypted_habit = encrypt_data(habit_text)

        db = get_db()
        db.execute("INSERT INTO habits (user_id, habit, date) VALUES (?, ?, DATE('now'))",
                   (user_id, encrypted_habit))
        db.commit()
        db.close()

        flash("Habit added successfully!")
        return redirect("/")
    return render_template("add_habit.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user with a hashed password (stored in the 'hash' column)."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return render_template("apology.html", message="Must provide username and password.")
        if password != confirmation:
            return render_template("apology.html", message="Passwords do not match.")

        hash_pw = generate_password_hash(password)
        db = get_db()
        try:
            # Note: We use column "hash" instead of "password"
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("apology.html", message="Username already taken.")
        finally:
            db.close()

        flash("Registered successfully! Please log in.")
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user by verifying the hashed password stored in 'hash'."""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("apology.html", message="Must provide username and password.")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()
        if user is None:
            return render_template("apology.html", message="Invalid username or password.")
        # Note: Use user["hash"] to check the password
        if not check_password_hash(user["hash"], password):
            return render_template("apology.html", message="Invalid username or password.")

        session["user_id"] = user["id"]
        flash("Logged in successfully!")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out the current user."""
    session.clear()
    flash("Logged out successfully!")
    return redirect("/login")

@app.route("/apology")
def apology():
    """Generic apology page."""
    message = request.args.get("message", "Something went wrong.")
    return render_template("apology.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
