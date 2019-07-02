from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

# DATABASE = 'sql/almoxarifado.db'
app = Flask(__name__)
# app.config.from_object(__name__)


conn = sqlite3.connect('sql/almoxarifado.db')

# cursor = conn.cursor()

#cur = cursor.execute("SELECT * from RECEPTACULO")
#print(cur.fetchall())


'''@app.route('/')
def hello():
    cur = cursor.execute("SELECT * from RECEPTACULO")
    print(cur.fetchall())
    pecas = [dict(upc=row[0]) for row in cur.fetchall()]
    print(pecas)
    # g.db.close()
    return render_template('teste.html', pecas=pecas)'''


@app.route('/teste')
def main():
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from RECEPTACULO")
        rows = x.fetchall()
        rec = [dict(tipo=row[0], corredor=row[1], ordem=row[2], qtd=row[3]) for row in rows]
        print(rec)
        con.commit()
        # msg = "Done"
        return render_template('index.html', rec=rec)


# def connet_db():
#     return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
