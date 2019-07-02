from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

DATABASE = 'sql/almoxarifado.db'
app = Flask(__name__)
app.config.from_object(__name__)


conn = sqlite3.connect('sql/almoxarifado.db')

cursor = conn.cursor()


@app.route('/')
def hello():
    # g.db = connet_db()
    cur = cursor.execute('select * from RECEPTACULO')
    print(cur.fetchall())
    conn.commit()
    pecas = [dict(upc=row[0]) for row in cur.fetchall()]
    print(pecas)
    # g.db.close()
    return render_template('teste.html', pecas=pecas)


# def connet_db():
#     return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
