# utils/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data/food_ratings.db")

def get_connection():
    """Create and return a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dict-like access
    return conn

def init_db():
    """Initialize the database with the required table."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TBL_FOOD_RATINGS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE TEXT,
        STORE_NAME TEXT,
        FOOD_NAME TEXT,
        CATEGORY TEXT,
        TASTE REAL,
        PRICE REAL,
        COMMENTS TEXT
    )
    """)

    # Lookup tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LOOKUP_CATEGORIES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LOOKUP_STORES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


def get_lookup_values(table_name):
    """Fetch lookup values from the given table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT NAME FROM {table_name} ORDER BY NAME")  # This line has been added or changed
    rows = [r[0] for r in cursor.fetchall()]
    conn.close()
    return rows


def insert_rating(date, store_name, food_name, category, taste, price, comments):
    """Insert a new food rating record."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO TBL_FOOD_RATINGS (DATE, STORE_NAME, FOOD_NAME, CATEGORY, TASTE, PRICE, COMMENTS)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, store_name, food_name, category, taste, price, comments))

    conn.commit()
    conn.close()


def fetch_all_ratings():
    """Retrieve all ratings."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TBL_FOOD_RATINGS ORDER BY DATE DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_lookup_value(table_name, name):
    """Add a new store or category if not exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO {table_name} (NAME) VALUES (?)", (name,))  # This line has been added or changed
    conn.commit()
    conn.close()