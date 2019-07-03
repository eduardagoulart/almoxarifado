import sqlite3

conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()

cursor.execute("""INSERT INTO RECEPTACULO VALUES('parafusos', 3, 01, 25)""")
cursor.execute("""INSERT INTO RECEPTACULO VALUES('caça', 2, 03, 10)""")
cursor.execute("""INSERT INTO RECEPTACULO VALUES('pesca', 4, 04, 35)""")
cursor.execute("""INSERT INTO RECEPTACULO VALUES('chave', 5, 05, 43)""")

cursor.execute("""INSERT INTO PEÇA VALUES(12345, 'rosca', 'Eduarda', 1, 'Distribuição')""")

cursor.execute(
    """
    INSERT INTO PEÇA VALUES(12346, 'porca', 'Luccas', 1, 'Distribuição')
    """
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12347, 'porca', 'Luccas', 1, 'Distribuição')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12348, 'porca', 'Luccas', 1, 'Distribuição')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12349, 'machado', 'Barbara', 2, 'Compra')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12350, 'prego', 'Eduarda', 3, 'Compra')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12351, 'martelo', 'Barbara', 4, 'Distribuição')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12352, 'chave de fenda', 'Luccas', 5, 'Compra')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12353, 'chave phillips', 'Luccas', 5, 'Distribuição')"""
)

cursor.execute(
    """INSERT INTO PEÇA VALUES(12354, 'chave inglesa', 'Eduarda', 2, 'Distribuição')"""
)

cursor.execute(
    """INSERT INTO ESTRADO VALUES(01, 12345, 25)"""
)

cursor.execute(
    """INSERT INTO ESTRADO VALUES(02, 12346, 15)"""
)

cursor.execute(
    """INSERT INTO ESTRADO VALUES(03, 12347, 18)"""
)

cursor.execute(
    """INSERT INTO ESTRADO VALUES(04, 12348, 35)"""
)

cursor.execute(
    """INSERT INTO ESTRADO VALUES(05, 12349, 20)"""
)

cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12345, 01, 01, 'parafusos')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12346, 02, 01, 'parafusos')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12347, 03, 01, 'parafusos')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12348, 04, 01, 'parafusos')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12349, 05, 02, 'caça')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12350, 06, 03, 'parafusos')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12351, 07, 05, 'caça')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12352, 08, 06, 'chave')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12353, 09, 06, 'chave')""")
cursor.execute("""INSERT INTO PECA_PEDIDO VALUES(12354, 10, 03, 'chave')""")


conn.commit()