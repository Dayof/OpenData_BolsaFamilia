# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# Criando a aplicação Flask
app = Flask(__name__)

app.config.from_envvar('BF_SETTINGS', silent=True)

print(app.config)

@app.route('/')
def index():
    db = getDB()
    cur = db.execute('select * from PAGAMENTO;')
    entries = cur.fetchall()
    return render_template('home.html', entries=entries)

@app.route('/all')
def allFav():
    db = getDB()
    cur = db.execute("""
        SELECT NOME_FAVORECIDO AS NIS,
        MUNICIPIO_CODIGO_SIAFI_MUNICIPIO AS Nome
        FROM FAVORECIDO
        ORDER BY nome ASC;
    """)
    entries = cur.fetchall()
    return render_template('all.html', entries=entries)

@app.route('/pay')
def highPay():
    db = getDB()
    cur = db.execute("""
        CREATE VIEW mais_favorecidos
        AS SELECT nis_favorecido AS NIS,
        nome_favorecido AS Nome,
        valor_parcela, mes_competencia
        FROM favorecido f
        JOIN pagamento
        ON nis = favorecido_nis_favorecido
        ORDER BY valor_parcela DESC;
    """)
    entries = cur.fetchall()
    return render_template('pay.html', entries=entries)

@app.route('/paystate')
def highPayState():
    db = getDB()
    cur = db.execute("""
        SELECT uf AS Estado,
        SUM(valor_parcela) AS Total
        FROM municipio
        LEFT JOIN favorecido
        ON nome_municipio = municipio_nome_municipio
        JOIN pagamento
        ON nis_favorecido = favorecido_nis_favorecido
        GROUP BY Estado;
    """)
    entries = cur.fetchall()
    return render_template('paystate.html', entries=entries)

@app.route('/addpag', methods=['POST'])
def addPag():
    db = getDB()

    db.execute('insert into FAVORECIDO (NIS_FAVORECIDO, NOME_FAVORECIDO, MUNICIPIO_CODIGO_SIAFI_MUNICIPIO) values (?, ?, ?)', [request.form['nis_fav'], request.form['nome_fav'], request.form['siafi']])

    db.commit()

    db.execute('insert into PAGAMENTO (PROGRAMA_CODIGO_PROGRAMA, FAVORECIDO_NIS_FAVORECIDO, MES_COMPETENCIA, VALOR_PARCELA) values (?, ?, ?, ?)', [request.form['cod_programa'], request.form['nis_fav'],
       request.form['mes'], request.form['valor']])
    db.commit()

    flash('Nova entrada de favorecido e pagamento foi adicionada!')

    return redirect(url_for('allFav'))

@app.route('/addfav', methods=['POST'])
def addFav():
    db = getDB()

    db.execute('insert into FAVORECIDO (NIS_FAVORECIDO, NOME_FAVORECIDO, MUNICIPIO_CODIGO_SIAFI_MUNICIPIO) values (?, ?, ?)', [request.form['siafi'], request.form['nis_fav'], request.form['nome_fav']])

    db.commit()

    flash('Nova entrada de favorecido foi adicionada!')

    return redirect(url_for('allFav'))

@app.route('/edit', methods=['POST'])
def editPag():
    db = getDB()

    db.execute("""
        update PAGAMENTO
        set VALOR_PARCELA = ?
        where PROGRAMA_CODIGO_PROGRAMA = ?
        and FAVORECIDO_NIS_FAVORECIDO = ?
        and MES_COMPETENCIA = ?
    """, (request.form['new_valor'], request.form['cod_programa'], request.form['nis_fav'], request.form['mes']))

    db.commit()

    flash('Valor da parcela de um pagamento foi editada com SUCESSO!!')
    print('Valor da parcela do favorecido %s para o valor de %s de um pagamento foi editado com SUCESSO!!' % (request.form['nis_fav'], request.form['valor']))

    return redirect(url_for('allFav'))

@app.route('/editfav', methods=['POST'])
def editFav():
    db = getDB()

    db.execute("""
        update FAVORECIDO
        set MUNICIPIO_CODIGO_SIAFI_MUNICIPIO = ?
        where NOME_FAVORECIDO = ?
    """, (request.form['nome_fav'], request.form['nis_fav']))

    db.commit()

    flash('Nome do favorecido editado com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.route('/del', methods=['POST'])
def delPag():
    db = getDB()

    db.execute("""
        delete from PAGAMENTO
        where PROGRAMA_CODIGO_PROGRAMA = ?
        and FAVORECIDO_NIS_FAVORECIDO = ?
        and MES_COMPETENCIA = ?
    """, (request.form['cod_programa'], request.form['nis_fav'], request.form['mes']))

    db.commit()

    flash('Pagamento foi deletado com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.route('/delfav', methods=['POST'])
def delFav():
    db = getDB()

    db.execute("""
        delete from FAVORECIDO
        where NOME_FAVORECIDO = ?
    """, (request.form['nis_fav'], ))

    db.commit()

    flash('Favorecido foi deletado com SUCESSO!!')

    return redirect(url_for('allFav'))

def connectDB():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def getDB():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connectDB()
    return g.sqlite_db

@app.teardown_appcontext
def closeDB(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    app.run(debug=True)
