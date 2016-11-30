import csv, sqlite3

to_db_bf, to_db_fav, to_db_pag = [], [], []

transf = lambda x: int(x.replace(',','')[:-3])

def insertMultTab(u, cs, n, cf, csf, cp, ca, ns, nf, f, v, m):
    to_db_bf.append((u, cs, n, cf, csf, cp, ca, ns, nf, f, v, m))
    to_db_fav.append((ns, nf, cs))
    to_db_pag.append((cp, nf, m, v))

conn = sqlite3.connect("all.db")
cur = conn.cursor()

print("DROPS NAS TABELAS DE FAVORECIDO E PAGAMENTO...")

cur.executescript("""
    DROP TABLE IF EXISTS `FAVORECIDO` ;
    DROP TABLE IF EXISTS `PAGAMENTO` ;
""")

print("DROPS NAS TABELAS DE FAVORECIDO E PAGAMENTO...COMPLETO")

print("DROPS NAS TABELAS PRIMÁRIAS...")

cur.executescript("""
    DROP TABLE IF EXISTS `BOLSA_FAMILIA` ;
    DROP TABLE IF EXISTS `FUNCAO_SUBFUNCAO` ;
""")

print("DROPS NAS TABELAS PRIMÁRIAS...COMPLETO")

print("CRIAÇÃO DAS TABELAS DE FAVORECIDO E PAGAMENTO...")

cur.executescript("""
    CREATE TABLE IF NOT EXISTS `FAVORECIDO` (
      `NIS_FAVORECIDO` VARCHAR(15) NOT NULL,
      `NOME_FAVORECIDO` VARCHAR(50) NULL,
      `CODIGO_SIAFI_MUNICIPIO` VARCHAR(4) NOT NULL,
      PRIMARY KEY (`NIS_FAVORECIDO`));

    CREATE TABLE IF NOT EXISTS `PAGAMENTO` (
        `COD_PAG` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
        `NIS_FAVORECIDO` VARCHAR(15) NOT NULL,
        `MES_COMPETENCIA` VARCHAR(10) NOT NULL,
        `VALOR_PARCELA` INTEGER NOT NULL);
""")

print("CRIAÇÃO DAS TABELAS DE FAVORECIDO E PAGAMENTO...COMPLETO")

print("CRIAÇÃO DAS TABELAS PRIMÁRIAS...")

cur.executescript("""
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
        VALOR_PARCELA INTEGER,
        MES_COMPETENCIA VARCHAR(10));

CREATE TABLE IF NOT EXISTS FUNCAO_SUBFUNCAO (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CODIGO_FUNCAO VARCHAR(2) NOT NULL,
        NOME_FUNCAO VARCHAR(50),
        CODIGO_SUBFUNCAO VARCHAR(3) NOT NULL,
        NOME_SUBFUNCAO VARCHAR(50));
""")

print("CRIAÇÃO DAS TABELAS PRIMÁRIAS...COMPLETO")

print("INSERT DO CSV DAS FUNÇÕES E SUBFUNCOES...")

with open('func_2015.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)
    to_db = [(i['CODIGO_FUNCAO'], i['NOME_FUNCAO'],
            i['CODIGO_SUBFUNCAO'], i['NOME_SUBFUNCAO']) for i in dr]

    if not to_db:
        print("OCORREU ERRO NO PROCESSAMENTO DA CSV DAS FUNCOES E SUBFUNCOES PARA TABELA FUNCAO_SUBFUNCAO...")
        exit()

cur.executemany("INSERT INTO FUNCAO_SUBFUNCAO ( \
                            CODIGO_FUNCAO, \
                            NOME_FUNCAO, \
                            CODIGO_SUBFUNCAO, \
                            NOME_SUBFUNCAO \
                            ) \
                            VALUES (?, ?, ?, ?);", to_db)
conn.commit()

print("INSERT DO CSV DAS FUNÇÕES...COMPLETO")

print("INSERT DO CSV DA BOLSA FAMÍLIA...")

print("EXTRAÇÃO NO CSV DA BOLSA FAMILIA...")

with open('bf.csv', encoding = "ISO-8859-1") as inf:
    dr = csv.DictReader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
    print(dr.fieldnames)

    [insertMultTab(i['UF'], i['CODIGO_SIAFI_MUNICIPIO'],
    i['NOME_MUNICIPIO'], i['CODIGO_FUNCAO'],
    i['CODIGO_SUBFUNCAO'], i['CODIGO_PROGRAMA'],
    i['CODIGO_ACAO'], i['NIS_FAVORECIDO'],
    i['NOME_FAVORECIDO'], i['FONTE_FINALIDADE'],
    transf(i['VALOR_PARCELA']), i['MES_COMPETENCIA']) for i in dr]

    if not to_db_bf:
        print("OCORREU ERRO NO PROCESSAMENTO DA CSV DA BF PARA TABELA BOLSA_FAMILIA...")
        exit()

    if not to_db_fav:
        print("OCORREU ERRO NO PROCESSAMENTO DA CSV DA BF PARA TABELA FAVORECIDO...")
        exit()

    if not to_db_pag:
        print("OCORREU ERRO NO PROCESSAMENTO DA CSV DA BF PARA TABELA PAGAMENTO...")
        exit()

print("EXTRAÇÃO NO CSV DA BOLSA FAMILIA...COMPLETO")

print("OBJETOS PYTHON PARA DB NA TABELA DE PAGAMENTOS...")

cur.executemany("INSERT INTO PAGAMENTO ( \
                            CODIGO_PROGRAMA, \
                            NIS_FAVORECIDO, \
                            MES_COMPETENCIA, \
                            VALOR_PARCELA \
                            ) \
                            VALUES (?, ?, ?, ?);", to_db_pag)

conn.commit()

print("OBJETOS PYTHON PARA DB NA TABELA DE PAGAMENTOS...COMPLETO")

print("OBJETOS PYTHON PARA DB NA TABELA DOS FAVORECIDOS...")

cur.executemany("INSERT OR IGNORE INTO FAVORECIDO ( \
                                        NIS_FAVORECIDO, \
                                        NOME_FAVORECIDO, \
                                        CODIGO_SIAFI_MUNICIPIO \
                                        ) \
                                        VALUES (?, ?, ?);", to_db_fav)
conn.commit()

print("OBJETOS PYTHON PARA DB NA TABELA DOS FAVORECIDOS...COMPLETO")

print("OBJETOS PYTHON PARA DB NA TABELA DO BOLSA FAMILIA...")

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
                                    ?, ?);", to_db_bf)

conn.commit()

print("OBJETOS PYTHON PARA DB NA TABELA DO BOLSA FAMILIA...COMPLETO")

conn.close()
