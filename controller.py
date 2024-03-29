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
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
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
    sqlite3.connect('sql/almoxarifado.db').close()
    return render_template('index.html', rec=rec)


@app.route('/pecas')
def pecas():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from PEÇA")
        rows = x.fetchall()
        pecas = [dict(upc=row[0], descricao=row[1], fornecedor=row[2], numero=row[3], setor_compra=row[4]) for row in
                 rows]
        con.commit()
    return render_template('pecas.html', pecas=pecas)


@app.route('/pecas_pedido')
def pecas_pedido():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from PECA_PEDIDO")
        rows = x.fetchall()
        peca = [dict(upc=row[0], n_pedido=row[1], n_estrado=row[2], tipo=row[3]) for row in rows]
        con.commit()
    return render_template('pecas_pedido.html', peca=peca)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            insert = [
                request.form['tipo'],
                request.form['corredor'],
                request.form['ordem'],
                request.form['qtd'],
            ]
            if None in insert:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('index'))
            else:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO RECEPTACULO (tipe_peças, corredor, ordem, quantidade_peças) values (?, ?, ?, ?)",
                    [insert[0], insert[1], insert[2], insert[3]])
                con.commit()
                # con.close()
                return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/add_pecas', methods=['GET', 'POST'])
@login_required
def add_pecas():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            insert = [
                request.form['upc'],
                request.form['descricao'],
                request.form['fornecedor'],
                request.form['numero'],
                request.form['setor_compra'],
            ]
            if None in insert:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas'))
            else:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO PEÇA (upc, descricao, fornecedor, numero, setor_compra) values (?, ?, ?, ?, ?)",
                    [insert[0], insert[1], insert[2], insert[3], insert[4]])
                con.commit()
                return redirect(url_for('pecas'))

    return render_template('add_pecas.html')


@app.route('/add_pecas_pedido', methods=['GET', 'POST'])
@login_required
def add_pecas_pedido():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            insert = [
                request.form['upc'],
                request.form['n_pedido'],
                request.form['n_estrado'],
                request.form['tipo'],
            ]
            if None in insert:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas_pedido'))
            else:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO PECA_PEDIDO (upc, n_pedido, n_estrado, tipo) values (?, ?, ?, ?)",
                    [insert[0], insert[1], insert[2], insert[3]])
                con.commit()
                return redirect(url_for('pecas_pedido'))

    return render_template('add_pecas_pedido.html')


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM RECEPTACULO WHERE tipe_peças='{request.form['tipo']}'")
            con.commit()
            return redirect(url_for('index'))
    return render_template('delete.html')


@app.route('/delete_pecas', methods=['GET', 'POST'])
@login_required
def delete_pecas():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM PEÇA WHERE upc='{request.form['upc']}'")
            con.commit()
            return redirect(url_for('pecas'))
    return render_template('delete_peca.html')


@app.route('/delete_pecas_pedido', methods=['GET', 'POST'])
@login_required
def delete_pecas_pedido():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM PECA_PEDIDO WHERE upc='{request.form['upc']}'")
            con.commit()
            return redirect(url_for('pecas_pedido'))
    return render_template('delete_pecas_pedido.html')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    sqlite3.connect('sql/almoxarifado.db').close()
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


@app.route('/update_pecas', methods=['GET', 'POST'])
@login_required
def update_pecas():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            up = [
                request.form['upc'],
                request.form['descricao'],
                request.form['fornecedor'],
                request.form['numero'],
                request.form['setor_compra'],
            ]
            if None in up:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas'))
            else:
                cur = con.cursor()
                cur.execute(
                    f"UPDATE PEÇA set descricao='{up[1]}', fornecedor='{up[2]}', numero={up[3]}, setor_compra='{up[4]}' WHERE upc={up[0]}")
                con.commit()
                return redirect(url_for('pecas'))

    return render_template('update_pecas.html')


@app.route('/update_pecas_pedido', methods=['GET', 'POST'])
@login_required
def update_pecas_pedido():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            up = [
                request.form['upc'],
                request.form['n_pedido'],
                request.form['n_estrado'],
                request.form['tipo']
            ]
            if None in up:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas_pedido'))
            else:
                cur = con.cursor()
                cur.execute(
                    f"UPDATE PECA_PEDIDO set n_pedido={up[1]}, n_estrado={up[2]}, tipo='{up[3]}' WHERE upc={up[0]}")
                con.commit()
                return redirect(url_for('pecas_pedido'))

    return render_template('update_pecas_pedido.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            tipo = request.form['tipo']
            corredor = request.form['corredor']
            ordem = request.form['ordem']
            qtd = request.form['qtd']
            values = ""
            if tipo:
                values += f"tipe_peças='{tipo}'"
            if corredor:
                if tipo:
                    values += f"AND corredor={int(corredor)}"
                else:
                    values += f"corredor={int(corredor)}"
            if ordem:
                if tipo or corredor:
                    values += f"AND ordem={int(ordem)}"
                else:
                    values += f"ordem={int(ordem)}"
            if qtd:
                if tipo or corredor or ordem:
                    values += f"AND quantidade_peças={int(qtd)}"
                else:
                    values += f"quantidade_peças={int(qtd)}"

            cur = con.cursor()
            x = cur.execute(f"SELECT * FROM RECEPTACULO WHERE {values}")
            rows = x.fetchall()
            values = [dict(tipo=row[0], corredor=row[1], ordem=row[2], qtd=row[3]) for row in rows]
            return render_template('result_search.html', values=values)
    return render_template('search.html')


@app.route('/p_aninhada', methods=['GET', 'POST'])
def pesquisa_aninhada():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            qtd = request.form['qtd']
            cur = con.cursor()
            e = int(qtd)
            x = cur.execute(
                f"SELECT p.upc, p.fornecedor, pp.tipo FROM PEÇA as p JOIN PECA_PEDIDO as pp on pp.upc = p.upc WHERE pp.tipo in (SELECT rec.tipe_peças FROM RECEPTACULO as rec WHERE quantidade_peças > {e})")
            rows = x.fetchall()
            values = [dict(upc=row[0], fornecedor=row[1], tipo=row[2]) for row in rows]
        return render_template('result_aninhada.html', values=values)
    return render_template('aninhada.html')


@app.route('/join')
def pesquisa_join():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT corredor, ordem, UPC FROM PECA_PEDIDO JOIN RECEPTACULO on tipo=tipe_peças")
        rows = x.fetchall()
        values = [dict(corredor=row[0], ordem=row[1], upc=row[2]) for row in rows]
    return render_template('result_join.html', values=values)


@app.route('/agregacao')
def pesquisa_agregacao():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT COUNT(*), fornecedor FROM PEÇA group by fornecedor;")
        rows = x.fetchall()
        values = [dict(value=row[0], nome=row[1]) for row in rows]
    return render_template('result_agregacao.html', values=values)


@app.route('/agregacao_rec')
def pesquisa_agregacao_rec():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT SUM(quantidade_peças), corredor, ordem FROM RECEPTACULO group by corredor, ordem;")
        rows = x.fetchall()
        values = [dict(value=row[0], corredor=row[1], ordem=row[2]) for row in rows]
    return render_template('agregacao_rec.html', values=values)


@app.route('/indo_pedido', methods=['GET', 'POST'])
def pesquisa_info_pedido():
    sqlite3.connect('sql/almoxarifado.db').close()
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            n_pedido = request.form['n_pedido']
            cur = con.cursor()
            pedido = int(n_pedido)
            x = cur.execute(
                f"select es.n_estrado,es.upc_peca,quantidade_pecas, corredor,ordem from ESTRADO as es join (select pc.n_estrado,n_pedido,ordem,corredor from RECEPTACULO as rc join PECA_PEDIDO as pc on rc.tipe_peças = pc.tipo where n_pedido = {pedido}) as tb on es.n_estrado = tb.n_estrado;"
            )
            rows = x.fetchall()
            values = [dict(n_estrado=row[0], upc=row[1], qtd=row[2], corredor=row[3], ordem=row[4])
                      for row in rows]
        return render_template('result_pedido.html', values=values)
    return render_template('pedido.html')


@app.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT * FROM info_rec")
        rows = x.fetchall()
        values = [dict(n_pedido=row[0], n_estrado=row[1], upc=row[2], qtd=row[3], corredor=row[4],
                       ordem=row[5]) for row in rows]
    return render_template('view.html', values=values)


@app.route('/view_pecas', methods=['GET', 'POST'])
@login_required
def view_pecas():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT * FROM info_pecas")
        rows = x.fetchall()
        values = [dict(upc=row[0], descricao=row[1], fornecedor=row[2], numero=row[3], setor_compra=row[4],
                       n_pedido=row[6], n_estrado=row[7], tipo=row[8]) for row in rows]
    return render_template('view_pecas.html', values=values)


if __name__ == '__main__':
    app.run(debug=True)
