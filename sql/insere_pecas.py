import sqlite3

conn = sqlite3.connect('sql/pecas.db')

cursor = conn.cursor()

cursor.execute(
    """INSERT INTO PEÇA VALUES(12345, 01, 'rosca', 'Eduarda', 1, 'Distribuição', 01, 'parafusos')"""
)

cursor.execute(
    """
    INSERT INTO PEÇA VALUES(12346, 02, 'porca', 'Luccas', 1, 'Distribuição', 01, 'parafusos');
    """
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12347, 03, 'porca', 'Luccas', 1, 'Distribuição', 01, 'parafusos')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12348, 04, 'porca', 'Luccas', 1, 'Distribuição', 01, 'parafusos')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12349, 05, 'machado', 'Barbara', 2, 'Compra', 02, 'caça')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12350, 06, 'prego', 'Eduarda', 3, 'Compra', 03, 'parafusos')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12351, 07, 'martelo', 'Barbara', 4, 'Distribuição', 05, 'caça')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12352, 08, 'chave de fenda', 'Luccas', 5, 'Compra', 06, 'chave')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12353, 09, 'chave phillips', 'Luccas', 5, 'Distribuição', 06, 'chave')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12354, 10, 'chave inglesa', 'Eduarda', 2, 'Distribuição', 03, 'chave')"""
)

conn.commit()