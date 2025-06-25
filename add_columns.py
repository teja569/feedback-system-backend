import sqlite3

conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

# Add reset_token column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    print("✅ Added 'reset_token' column.")
except sqlite3.OperationalError:
    print("ℹ️ 'reset_token' column already exists.")

# Add reset_token_expiry column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME")
    print("✅ Added 'reset_token_expiry' column.")
except sqlite3.OperationalError:
    print("ℹ️ 'reset_token_expiry' column already exists.")

conn.commit()
conn.close()
