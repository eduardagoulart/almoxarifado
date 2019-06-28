import sqlite3

conn = sqlite3.connect('sql/pecas.db')

cursor = conn.cursor()

cursor.execute("SELECT ")