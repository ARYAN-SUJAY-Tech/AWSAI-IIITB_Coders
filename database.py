import sqlite3
import os

# -----------------------------
# Database Path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            issue TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Create User
# -----------------------------
def create_user(email, username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE email=?", (email,))
    if cur.fetchone():
        conn.close()
        return "exists"

    cur.execute(
        "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
        (email, username, password)
    )
    conn.commit()
    conn.close()
    return "created"


# -----------------------------
# Authenticate User
# -----------------------------
def authenticate_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()
    return user


# -----------------------------
# Verify User (for password reset)
# -----------------------------
def verify_user(email, username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND username=?",
        (email, username)
    )
    user = cur.fetchone()
    conn.close()
    return user is not None


# -----------------------------
# Reset Password
# -----------------------------
def reset_password(email, new_password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE email=?",
        (new_password, email)
    )

    conn.commit()
    conn.close()
    return True


# -----------------------------
# Save History
# -----------------------------
def save_history(email, issue):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO history (email, issue) VALUES (?, ?)",
        (email, issue)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Get History
# -----------------------------
def get_history(email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT issue FROM history WHERE email=? ORDER BY id DESC",
        (email,)
    )

    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]
