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
        pecas = [dict(upc=row[0], n=row[1], descricao=row[2], fornecedor=row[3], numero=row[4], setor_compra=row[5],
                      estrado=row[6], tipo=row[7]) for row in rows]
        con.commit()
    return render_template('pecas.html', pecas=pecas)


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
    insert = [
        request.form['upc'],
        request.form['n_pedido'],
        request.form['descricao'],
        request.form['fornecedor'],
        request.form['numero'],
        request.form['setor_compra'],
        request.form['n_estrado'],
        request.form['tipo']
    ]
    if request.method == 'POST':
        with sqlite3.connect('sql/almoxarifado.db') as con:
            if None in insert:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas'))
            else:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO PEÇA (upc, n_pedido, descricao, fornecedor, numero, setor_compra, n_estrado, tipo) values (?, ?, ?, ?, ?, ?, ?, ?)",
                    [insert[0], insert[1], insert[2], insert[2], insert[3], insert[4], insert[5], insert[6], insert[7]])
                con.commit()
                flash("Novo valor adicionado com sucesso!!")
                return redirect(url_for('pecas'))

    return render_template('add_pecas.html')


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
            upc = request.form['upc']
            n_pedido = request.form['n_pedido']
            desc = request.form['descricao']
            fornecedor = request.form['fornecedor']
            numero = request.form['numero']
            setor_compra = request.form['setor_compra']
            n_estrado = request.form['n_estrado']
            tipo = request.form['tipo']
            if not tipo or not upc or not n_pedido or not desc or not fornecedor or not numero or not setor_compra or not n_estrado:
                flash("Por favor preencha todos os campos")
                return redirect(url_for('pecas'))
            else:
                cur = con.cursor()
                cur.execute(
                    f"UPDATE PEÇA set n_pedido={n_pedido}, descricao='{desc}', fornecedor='{fornecedor}', numero={numero}, setor_compra='{setor_compra}', n_estrado={n_estrado}, tipo='{tipo}'  WHERE upc={upc}")
                con.commit()
                return redirect(url_for('pecas'))

    return render_template('update_pecas.html')


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
                f"SELECT DISTINCT descricao FROM PEÇA WHERE tipo in (SELECT tipe_peças FROM RECEPTACULO WHERE quantidade_peças > {e});")
            rows = x.fetchall()
            values = [dict(descricao=row[0]) for row in rows]
        return render_template('result_aninhada.html', values=values)
    return render_template('aninhada.html')


@app.route('/join')
def pesquisa_join():
    sqlite3.connect('sql/almoxarifado.db').close()
    with sqlite3.connect('sql/almoxarifado.db') as con:
        cur = con.cursor()
        x = cur.execute(
            f"SELECT corredor, ordem, UPC FROM PEÇA JOIN RECEPTACULO on tipo=tipe_peças")
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
                f"select descricao,es.n_estrado,es.upc_peca,quantidade_pecas, corredor,ordem from ESTRADO as es join (select pc.n_estrado,n_pedido,ordem,corredor,descricao from RECEPTACULO as rc join PEÇA as pc on rc.tipe_peças = pc.tipo  where n_pedido = {pedido}) as tb on es.n_estrado = tb.n_estrado; "
            )
            rows = x.fetchall()
            values = [dict(descricao=row[0], n_estrado=row[1], upc=row[2], qtd=row[3], corredor=row[4], ordem=row[5])
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
            f"SELECT * FROM info_pecas")
        rows = x.fetchall()
        values = [dict(n_pedido=row[0], descricao=row[1], n_estrado=row[2], upc=row[3], qtd=row[4], corredor=row[5],
                       ordem=row[6]) for row in rows]
    return render_template('view.html', values=values)


if __name__ == '__main__':
    app.run(debug=True)
