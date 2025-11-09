import sqlite3

conn = sqlite3.connect('forum.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Show all users
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

print("All users in database:")
for user in users:
    print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}, Password: {user['password']}")

conn.close()