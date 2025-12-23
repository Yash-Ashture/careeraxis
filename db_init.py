import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    age INTEGER,
    location TEXT,
    skills TEXT,
    education TEXT
)
""")

conn.commit()
conn.close()

print("Profiles table created")
