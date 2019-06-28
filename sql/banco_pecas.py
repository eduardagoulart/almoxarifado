import sqlite3

conn = sqlite3.connect('sql/pecas.db')

cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE PEÇA (upc INT PRIMARY KEY, nº pedido INT UNIQUE, descricao TEXT, fornecedor VARCHAR(45), numero INT,
        setor_compra VARCHAR(45), nº_estrado INT, tipo VARCHAR(45))""")