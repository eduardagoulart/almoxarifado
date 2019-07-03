import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE PEÇA (upc INT PRIMARY KEY, nº pedido INT UNIQUE, descricao TEXT, fornecedor VARCHAR(45), numero INT,
        setor_compra VARCHAR(45), nº_estrado INT, tipo VARCHAR(45))""")

cursor.execute(
     """CREATE TABLE RECEPTACULO (tipe_peças VARCHAR(45) PRIMARY KEY, corredor INT, ordem INT, quantidade_peças INT)"""
)

cursor.execute(
    """CREATE TABLE ESTRADO (n_estrado INT PRIMARY KEY, upc_peca INT, quantidade_pecas INT)"""
)