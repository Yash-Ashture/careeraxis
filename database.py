import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

# Jobs table
cur.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    description TEXT
)
""")

# Applications table
cur.execute("""
CREATE TABLE IF NOT EXISTS applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    job_id INTEGER,
    status TEXT
)
""")

# ✅ Profiles table (ADD HERE, BEFORE close)
cur.execute("""
CREATE TABLE IF NOT EXISTS profiles(
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    location TEXT,
    education TEXT,
    skills TEXT,
    photo TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")
