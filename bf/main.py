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
    cur = db.execute('select * from MUNICIPIO;')
    entries = cur.fetchall()
    return render_template('home.html', entries=entries)

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

if __name__ == '__main__':
    app.run(debug=True)
