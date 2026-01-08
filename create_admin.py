import sqlite3
from werkzeug.security import generate_password_hash

ADMIN_ID = "stumna"
ADMIN_PW = "whdwhdwhd1%"

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("SELECT id FROM users WHERE username=?", (ADMIN_ID,))
row = cur.fetchone()

if row:
    print("admin already exists")
else:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (ADMIN_ID, generate_password_hash(ADMIN_PW), "admin")
    )
    conn.commit()
    print("admin created")

conn.close()

