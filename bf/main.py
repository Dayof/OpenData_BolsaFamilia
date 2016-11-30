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

def getDB():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        rv = connectDB()
        rv.row_factory = sqlite3.Row
        g.sqlite_db = rv.row_factory

    return g.sqlite_db

def getCON():
    if not hasattr(g, 'sqlite_db'):
        rv = connectDB()
        rv.row_factory = sqlite3.Row
        g.sqlite_db = rv.row_factory
    return rv

def connectDB():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv

def _searchFav(nis):
    db = getDB()
    cur = db.execute("""
            SELECT
                NOME_FAVORECIDO AS nome
            FROM
                FAVORECIDO
            WHERE
                NIS_FAVORECIDO = ?;
        """,(nis,))
    entries = cur.fetchall()
    return entries[0][0]

@app.route('/')
def index():
    db = getDB()
    con = getCON()

    con.create_function("search", 1, _searchFav)
    cur = db.execute("""
            SELECT
                search(NIS_FAVORECIDO) as nome,
                NIS_FAVORECIDO AS nis,
                MES_COMPETENCIA as mes,
                VALOR_PARCELA as valor
            FROM
                PAGAMENTO;
        """)
    entries = cur.fetchall()
    return render_template('home.html', entries=entries)

@app.route('/all')
def allFav():
    db = getDB()
    cur = db.execute("""
        SELECT
            NOME_FAVORECIDO AS nis,
            CODIGO_SIAFI_MUNICIPIO AS nome
        FROM
            FAVORECIDO
        ORDER BY nome ASC;
    """)
    entries = cur.fetchall()
    return render_template('all.html', entries=entries)

@app.route('/pay')
def highPay():
    db = getDB()
    cur = db.execute("""
        SELECT
            *
        FROM
            MAIS_FAVORECIDOS;
    """)
    entries = cur.fetchall()
    return render_template('pay.html', entries=entries)

@app.route('/paystate')
def highPayState():
    db = getDB()
    cur = db.execute("""
        SELECT
            m.uf AS estado,
            SUM(p.valor_parcela) AS total
        FROM
            MUNICIPIO m
        LEFT JOIN FAVORECIDO f ON f.CODIGO_SIAFI_MUNICIPIO = m.CODIGO_SIAFI_MUNICIPIO
        JOIN PAGAMENTO p ON f.nis_favorecido = p.nis_favorecido
        GROUP BY
            estado;
    """)
    entries = cur.fetchall()
    return render_template('paystate.html', entries=entries)

@app.route('/allfavbystate')
def allFavByState():
    db = getDB()
    cur = db.execute("""
        SELECT
            m.uf as estado,
            COUNT(p.codigo_siafi_municipio) AS total_fav
        FROM
            MUNICIPIO m
        LEFT JOIN FAVORECIDO f ON m.codigo_siafi_municipio = f.codigo_siafi_municipio
        GROUP BY
            estado
        ORDER BY
            total_fav;
    """)
    entries = cur.fetchall()
    return render_template('allfavbystate.html', entries=entries)

@app.route('/medvalor')
def medValor():
    db = getDB()
    cur = db.execute("""
        SELECT
            AVG(valor_parcela) AS med_pag
        FROM
            PAGAMENTO;
    """)
    entries = cur.fetchall()
    return render_template('medvalor.html', entries=entries)

@app.route('/medvalorbystate')
def medValorEstado():
    db = getDB()
    cur = db.execute("""
        SELECT
            m.uf AS estado,
            AVG(p.valor_parcela) AS med_state
        FROM
            MUNICIPIO m
        LEFT JOIN FAVORECIDO f ON m.codigo_siafi_municipio = f.codigo_siafi_municipio
        LEFT JOIN PAGAMENTO p ON f.nis_favorecido = p.nis_favorecido
        GROUP BY
            estado
        ORDER BY
            med_state;
    """)
    entries = cur.fetchall()
    return render_template('medvalorbystate.html', entries=entries)

@app.route('/addpag', methods=['POST'])
def addPag():
    db = getDB()
    db.execute("""
        INSERT INTO FAVORECIDO (NIS_FAVORECIDO, NOME_FAVORECIDO, CODIGO_SIAFI_MUNICIPIO)
        VALUES (?, ?, ?);
        """, [request.form['nis_fav'], request.form['nome_fav'], request.form['siafi']])

    db.commit()

    db.execute("""
        INSERT INTO PAGAMENTO (CODIGO_PROGRAMA, NIS_FAVORECIDO, MES_COMPETENCIA, VALOR_PARCELA)
        VALUES (?, ?, ?, ?);
        """, [request.form['cod_programa'], request.form['nis_fav'],
       request.form['mes'], request.form['valor']])

    db.commit()

    flash('Nova entrada de favorecido e pagamento foi adicionada!')

    return redirect(url_for('allFav'))

@app.route('/addfav', methods=['POST'])
def addFav():
    db = getDB()

    db.execute("""
        INSERT INTO FAVORECIDO (NIS_FAVORECIDO, NOME_FAVORECIDO, CODIGO_SIAFI_MUNICIPIO)
        VALUES (?, ?, ?);
        """, [request.form['nis_fav'], request.form['nome_fav'], request.form['siafi']])

    db.commit()

    flash('Nova entrada de favorecido foi adicionada!')

    return redirect(url_for('allFav'))

# TODO - exibir as rows encontradas com os valores inseridos e selecionar qual dado de pagamento editar
@app.route('/edit', methods=['POST'])
def editPag():
    db = getDB()

    db.execute("""
        UPDATE
            PAGAMENTO
        SET
            VALOR_PARCELA = ?
        WHERE
            CODIGO_PROGRAMA = ?
        AND
            NIS_FAVORECIDO = ?
        AND
            MES_COMPETENCIA = ?;
    """, (request.form['new_valor'], request.form['cod_programa'], request.form['nis_fav'], request.form['mes']))

    db.commit()

    flash('Valor da parcela de um pagamento foi editada com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.route('/editfav', methods=['POST'])
def editFav():
    db = getDB()

    db.execute("""
        UPDATE
            FAVORECIDO
        SET
            NOME_FAVORECIDO = ?
        WHERE
            NIS_FAVORECIDO = ?
    """, (request.form['nome_fav'], request.form['nis_fav']))

    db.commit()

    flash('Nome do favorecido editado com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.route('/del', methods=['POST'])
def delPag():
    db = getDB()

    db.execute("""
        DELETE FROM
            PAGAMENTO
        WHERE
            CODIGO_PROGRAMA = ?
        AND
            NIS_FAVORECIDO = ?
        AND
            MES_COMPETENCIA = ?
    """, (request.form['cod_programa'], request.form['nis_fav'], request.form['mes']))

    db.commit()

    flash('Pagamento foi deletado com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.route('/delfav', methods=['POST'])
def delFav():
    db = getDB()

    db.execute("""
        DELETE FROM
            FAVORECIDO
        WHERE
            NIS_FAVORECIDO = ?
    """, (request.form['nis_fav'], ))

    db.commit()

    flash('Favorecido foi deletado com SUCESSO!!')

    return redirect(url_for('allFav'))

@app.teardown_appcontext
def closeDB(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    app.run(debug=True)
