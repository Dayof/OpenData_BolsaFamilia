import csv, sqlite3

conn = sqlite3.connect("bf.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS FAVORECIDOS (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        UF VARCHAR(2),
        CODIGO_SIAFI_MUNICIPIO VARCHAR(10),
        NOME_MUNICIPIO VARCHAR(20),
        CODIGO_FUNCAO VARCHAR(5),
        CODIGO_SUBFUNCAO VARCHAR(10),
        CODIGO_PROGRAMA VARCHAR(10),
        CODIGO_ACAO VARCHAR(10),
        NIS_FAVORECIDO VARCHAR(20),
        NOME_FAVORECIDO VARCHAR(50) NOT NULL,
        FONTE_FINALIDADE VARCHAR(40),
        VALOR_PARCELA VARCHAR(10),
        MES_COMPETENCIA VARCHAR(7)
);
""")

with open('bf.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)
    to_db = [(i['UF'], i['CODIGO_SIAFI_MUNICIPIO'],
            i['NOME_MUNICIPIO'], i['CODIGO_FUNCAO'],
            i['CODIGO_SUBFUNCAO'], i['CODIGO_PROGRAMA'],
            i['CODIGO_ACAO'], i['NIS_FAVORECIDO'],
            i['NOME_FAVORECIDO'], i['FONTE_FINALIDADE'],
            i['VALOR_PARCELA'], i['MES_COMPETENCIA']) for i in dr]

cur.executemany("INSERT INTO FAVORECIDOS ( \
                                UF, \
                                CODIGO_SIAFI_MUNICIPIO, \
                                NOME_MUNICIPIO, \
                                CODIGO_FUNCAO, \
                                CODIGO_SUBFUNCAO, \
                                CODIGO_PROGRAMA, \
                                CODIGO_ACAO, \
                                NIS_FAVORECIDO, \
                                NOME_FAVORECIDO, \
                                FONTE_FINALIDADE, \
                                VALOR_PARCELA, \
                                MES_COMPETENCIA \
                                ) \
                                VALUES (?, ?, ?, ?, ?, \
                                        ?, ?, ?, ?, ?, \
                                        ?, ?);", to_db)
conn.commit()
conn.close()
