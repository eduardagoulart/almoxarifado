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
        # name = "bob"
        cur = con.cursor()
        x = cur.execute("SELECT * from RECEPTACULO")
        print(x.fetchall())
        rows = x.fetchall()
        print(type(x.fetchall()))
        for i in rows:
            print('ta entrando aqui')
            print(f'i: {i}')
        rec = [dict(upc=row[0], n=row[1]) for row in x.fetchall()]
        print(rec)
        con.commit()
        # msg = "Done"
        return render_template('teste.html', rec=rec)


# def connet_db():
#     return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
