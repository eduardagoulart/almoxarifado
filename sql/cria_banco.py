import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE PEÇA (upc INT PRIMARY KEY, n_pedido INT UNIQUE, descricao TEXT, fornecedor VARCHAR(45), numero INT,
        setor_compra VARCHAR(45), n_estrado INT, tipo VARCHAR(45))""")

cursor.execute(
    """CREATE TABLE RECEPTACULO (tipe_peças VARCHAR(45) PRIMARY KEY, corredor INT, ordem INT, quantidade_peças INT)"""
)

cursor.execute(
    """CREATE TABLE ESTRADO (n_estrado INT PRIMARY KEY, upc_peca INT, quantidade_pecas INT)"""
)

cursor.execute(
    """CREATE VIEW info_pecas as select n_pedido, descricao,es.n_estrado,es.upc_peca,quantidade_pecas, corredor,ordem 
    from ESTRADO as es join (select pc.n_estrado,n_pedido,ordem,corredor,descricao from RECEPTACULO as rc join PEÇA as 
    pc on rc.tipe_peças = pc.tipo) as tb on es.n_estrado = tb.n_estrado"""
)
