import csv, sqlite3

conn = sqlite3.connect("bf.db")
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS `BOLSA_FAMILIA` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `FUNCAO_SUBFUNCAO` ;
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS BOLSA_FAMILIA (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        UF VARCHAR(2),
        CODIGO_SIAFI_MUNICIPIO VARCHAR(4),
        NOME_MUNICIPIO VARCHAR(15),
        CODIGO_FUNCAO VARCHAR(2),
        CODIGO_SUBFUNCAO VARCHAR(3),
        CODIGO_PROGRAMA VARCHAR(4),
        CODIGO_ACAO VARCHAR(4),
        NIS_FAVORECIDO VARCHAR(15),
        NOME_FAVORECIDO VARCHAR(50) NOT NULL,
        FONTE_FINALIDADE VARCHAR(50),
        VALOR_PARCELA VARCHAR(8),
        MES_COMPETENCIA VARCHAR(10)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS FUNCAO_SUBFUNCAO (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CODIGO_FUNCAO VARCHAR(2) NOT NULL,
        NOME_FUNCAO VARCHAR(50),
        CODIGO_SUBFUNCAO VARCHAR(3) NOT NULL,
        NOME_SUBFUNCAO VARCHAR(50)
);
""")

print("TABELAS PRIMÁRIAS CRIADAS!")

with open('func_2015.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)
    to_db = [(i['CODIGO_FUNCAO'], i['NOME_FUNCAO'],
            i['CODIGO_SUBFUNCAO'], i['NOME_SUBFUNCAO']) for i in dr]

cur.executemany("INSERT INTO FUNCAO_SUBFUNCAO ( \
                            CODIGO_FUNCAO, \
                            NOME_FUNCAO, \
                            CODIGO_SUBFUNCAO, \
                            NOME_SUBFUNCAO \
                            ) \
                            VALUES (?, ?, ?, ?);", to_db)

conn.commit()
print("INSERT DO CSV DAS FUNÇÕES COMPLETO!")

with open('bf.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)
    to_db = [(i['UF'], i['CODIGO_SIAFI_MUNICIPIO'],
            i['NOME_MUNICIPIO'], i['CODIGO_FUNCAO'],
            i['CODIGO_SUBFUNCAO'], i['CODIGO_PROGRAMA'],
            i['CODIGO_ACAO'], i['NIS_FAVORECIDO'],
            i['NOME_FAVORECIDO'], i['FONTE_FINALIDADE'],
            i['VALOR_PARCELA'], i['MES_COMPETENCIA']) for i in dr]

cur.executemany("INSERT INTO BOLSA_FAMILIA ( \
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
print("INSERT DO CSV DA BOLSA FAMÍLIA COMPLETO!")

conn.close()
