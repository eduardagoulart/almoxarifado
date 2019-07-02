import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()

x = cursor.execute("SELECT * from RECEPTACULO")
tipo = "'duda'"
corredor = 5
ordem = 12389
qtd = 34
# y = cursor.execute(f"UPDATE RECEPTACULO set tipe_peças={tipo}, corredor = {corredor}, ordem={ordem}, quantidade_
# peças={qtd} WHERE tipe_peças={tipo}")

cursor.execute(
    f"UPDATE RECEPTACULO set corredor = {corredor}, ordem={ordem}, quantidade_peças={qtd} WHERE tipe_peças={tipo}")
# print(z.fetchall())
conn.commit()
z = cursor.execute("SELECT * from RECEPTACULO")
print(z.fetchall())
