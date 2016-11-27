import csv, sqlite3

conn = sqlite3.connect("func_2015.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS FUNCAO (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CODIGO_FUNCAO VARCHAR(2) NOT NULL,
        NOME_FUNCAO VARCHAR(30),
        CODIGO_SUBFUNCAO VARCHAR(3) NOT NULL,
        NOME_SUBFUNCAO VARCHAR(50)
);
""")

with open('func_2015.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)
    to_db = [(i['CODIGO_FUNCAO'], i['NOME_FUNCAO'],
            i['CODIGO_SUBFUNCAO'], i['NOME_SUBFUNCAO']) for i in dr]

cur.executemany("INSERT INTO FUNCAO ( \
                                CODIGO_FUNCAO, \
                                NOME_FUNCAO, \
                                CODIGO_SUBFUNCAO, \
                                NOME_SUBFUNCAO \
                                ) \
                                VALUES (?, ?, ?, ?);", to_db)
conn.commit()
conn.close()
