from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

# DATABASE = 'sql/almoxarifado.db'
app = Flask(__name__)
SECRET_KEY = 'tp_bd'
app.config.from_object(__name__)

conn = sqlite3.connect('sql/almoxarifado.db')

# cursor = conn.cursor()

# cur = cursor.execute("SELECT * from RECEPTACULO")
# print(cur.fetchall())


'''@app.route('/')
def hello():
    cur = cursor.execute("SELECT * from RECEPTACULO")
    print(cur.fetchall())
    pecas = [dict(upc=row[0]) for row in cur.fetchall()]
    print(pecas)
    # g.db.close()
    return render_template('teste.html', pecas=pecas)'''


@app.route('/', methods=['GET', 'POST'])
def index():
    with sqlite3.connect("sql/almoxarifado.db") as con:
        cur = con.cursor()
        x = cur.execute("SELECT * from RECEPTACULO")
        rows = x.fetchall()
        rec = [dict(tipo=row[0], corredor=row[1], ordem=row[2], qtd=row[3]) for row in rows]
        print(request.method)
        if request.method == 'POST':
            print("OI")
            with sqlite3.connect('sql/almoxarifado.db') as con:
                cur = con.cursor()
                #cur.execute(
                #    f"DELETE FROM RECEPTACULO WHERE tipe_peças='{request.form['tipo']}'")
                print('oh nois aqui')
                return redirect(url_for('index'))
        con.commit()

    return render_template('index.html', rec=rec)


@app.route('/add', methods=['GET', 'POST'])
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


# def connet_db():
#     return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
