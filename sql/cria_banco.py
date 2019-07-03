import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE PEÇA (upc INT PRIMARY KEY, descricao TEXT, fornecedor VARCHAR(45), numero INT, 
    setor_compra VARCHAR(45))""")

cursor.execute(
    """CREATE TABLE PECA_PEDIDO (upc INT PRIMARY KEY, n_pedido INT UNIQUE,  n_estrado INT, tipo VARCHAR(45))"""
)

cursor.execute(
    """CREATE TABLE RECEPTACULO (tipe_peças VARCHAR(45) PRIMARY KEY, corredor INT, ordem INT, quantidade_peças INT)"""
)

cursor.execute(
    """CREATE TABLE ESTRADO (n_estrado INT PRIMARY KEY, upc_peca INT, quantidade_pecas INT)"""
)

cursor.execute(
    """CREATE VIEW info_rec as select n_pedido,es.n_estrado,es.upc_peca,quantidade_pecas, corredor,ordem 
    from ESTRADO as es join (select pc.n_estrado,n_pedido,ordem,corredor from RECEPTACULO as rc join PECA_PEDIDO as 
    pc on rc.tipe_peças = pc.tipo) as tb on es.n_estrado = tb.n_estrado"""
)

cursor.execute(
    """CREATE VIEW info_pecas as select * from PEÇA as p JOIN PECA_PEDIDO as pp on p.upc = pp.upc"""
)