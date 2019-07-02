import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()

x = cursor.execute("SELECT * from RECEPTACULO")
print(x.fetchall())