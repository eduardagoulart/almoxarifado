from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# DATABASE = 'sql/almoxarifado.db'
app = Flask(__name__)
SECRET_KEY = 'tp_bd'
USERNAME = 'admin'
PASSWORD = 'admin'
app.config.from_object(__name__)

conn = sqlite3.connect('sql/almoxarifado.db')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Dados inválidos. Tente novamente!'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('loggin.html', error=error), status_code


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Você saiu do sistema")
    return redirect(url_for('login'))


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwards):
        if 'logged_in' in session:
            return test(*args, **kwards)
        else:
            return redirect(url_for('login'))

    return wrap


@app.route('/receptaculo', methods=['GET', 'POST'])
def index():
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from RECEPTACULO")
        rows = x.fetchall()
        rec = [dict(tipo=row[0], corredor=row[1], ordem=row[2], qtd=row[3]) for row in rows]
        con.commit()

    return render_template('index.html', rec=rec)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            tipo = request.form['tipo']
            corredor = request.form['corredor']
            ordem = request.form['ordem']
            qtd = request.form['qtd']
            if not tipo or not corredor or not ordem or not qtd:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('index'))
            else:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO RECEPTACULO (tipe_peças, corredor, ordem, quantidade_peças) values (?, ?, ?, ?)",
                    [tipo, corredor, ordem, qtd])
                con.commit()
                flash("Novo valor adicionado com sucesso!!")
                return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM RECEPTACULO WHERE tipe_peças='{request.form['tipo']}'")
            con.commit()
            return redirect(url_for('index'))
    return render_template('delete.html')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            tipo = request.form['tipo']
            corredor = request.form['corredor']
            ordem = request.form['ordem']
            qtd = request.form['qtd']
            if not tipo or not corredor or not ordem or not qtd:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('index'))
            else:
                cur = con.cursor()
                cur.execute(
                    f"UPDATE RECEPTACULO set corredor = {corredor}, ordem={ordem}, quantidade_peças={qtd} WHERE tipe_peças='{tipo}'")
                con.commit()
                flash("Novo valor editado com sucesso!!")
                return redirect(url_for('index'))

    return render_template('update.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            tipo = request.form['tipo']
            corredor = request.form['corredor']
            ordem = request.form['ordem']
            qtd = request.form['qtd']
            print('entra aqui')
            values = ""
            if tipo:
                values += f"tipe_peças='{tipo}'"
            if corredor:
                if tipo:
                    values += f"AND corredor={corredor}"
                else:
                    values += f"corredor={corredor}"
            if ordem:
                if tipo or corredor:
                    values += f"AND ordem={ordem}"
                else:
                    values += f"ordem={ordem}"
            if qtd:
                if tipo or corredor or ordem:
                    values += f"AND quantidade_peças={qtd}"
                else:
                    values += f"quantidade_peças={qtd}"

            cur = con.cursor()
            x = cur.execute(f"SELECT * FROM RECEPTACULO WHERE {values}")
            rows = x.fetchall()
            values = [dict(tipo=row[0], corredor=row[1], ordem=row[2], qtd=row[3]) for row in rows]
            return render_template('result_search.html', values=values)
    return render_template('search.html')


@app.route('/pecas')
def pecas():
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from PEÇA")
        rows = x.fetchall()
        pecas = [dict(upc=row[0], n=row[1], descricao=row[2], fornecedor=row[3], numero=row[4], setor_compra=row[5],
                      estrado=row[6], tipo=row[7]) for row in rows]
        print(pecas)
        con.commit()
    return render_template('pecas.html', pecas=pecas)


# def connet_db():
#     return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
