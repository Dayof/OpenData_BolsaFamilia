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
DROP TABLE IF EXISTS `FAVORECIDOS` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `MUNICIPIO` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `FAVORECIDO` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `PROGRAMA` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `PAGAMENTO` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `FUNCAO` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `SUBFUNCAO` ;
""")
cur.execute("""
DROP TABLE IF EXISTS `ACAO` ;
""")

cur.execute("""
    -- -----------------------------------------------------
    -- Table `MUNICIPIO`
    -- -----------------------------------------------------
    CREATE TABLE IF NOT EXISTS `MUNICIPIO` (
        `CODIGO_SIAFI_MUNICIPIO` VARCHAR(4) NOT NULL,
        `NOME_MUNICIPIO` VARCHAR(15) NULL,
        `UF` VARCHAR(2) NULL,
        PRIMARY KEY (`CODIGO_SIAFI_MUNICIPIO`));
""")

cur.execute("""
    -- -----------------------------------------------------
    -- Table `FAVORECIDO`
    -- -----------------------------------------------------
    CREATE TABLE IF NOT EXISTS `FAVORECIDO` (
      `NIS_FAVORECIDO` VARCHAR(15) NOT NULL,
      `NOME_FAVORECIDO` VARCHAR(40) NULL,
      `MUNICIPIO_CODIGO_SIAFI_MUNICIPIO` VARCHAR(4) NOT NULL,
      PRIMARY KEY (`NIS_FAVORECIDO`),
      CONSTRAINT `fk_FAVORECIDO_MUNICIPIO`
        FOREIGN KEY (`MUNICIPIO_CODIGO_SIAFI_MUNICIPIO`)
        REFERENCES `MUNICIPIO` (`CODIGO_SIAFI_MUNICIPIO`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);
""")

cur.execute("""
-- -----------------------------------------------------
-- Table `PROGRAMA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PROGRAMA` (
  `CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
  `NOME_PROGRAMA` VARCHAR(40) NULL,
  PRIMARY KEY (`CODIGO_PROGRAMA`));
""")

cur.execute("""
-- -----------------------------------------------------
-- Table `PAGAMENTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PAGAMENTO` (
  `PROGRAMA_CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
  `FAVORECIDO_NIS_FAVORECIDO` VARCHAR(15) NOT NULL,
  `MES_COMPETENCIA` VARCHAR(10) NOT NULL,
  `VALOR_PARCELA` VARCHAR(8) NULL,
  PRIMARY KEY (`PROGRAMA_CODIGO_PROGRAMA`, `FAVORECIDO_NIS_FAVORECIDO`, `MES_COMPETENCIA`),
  CONSTRAINT `fk_PROGRAMA_has_FAVORECIDO_PROGRAMA1`
    FOREIGN KEY (`PROGRAMA_CODIGO_PROGRAMA`)
    REFERENCES `PROGRAMA` (`CODIGO_PROGRAMA`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PROGRAMA_has_FAVORECIDO_FAVORECIDO1`
    FOREIGN KEY (`FAVORECIDO_NIS_FAVORECIDO`)
    REFERENCES `FAVORECIDO` (`NIS_FAVORECIDO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
""")

cur.execute("""
-- -----------------------------------------------------
-- Table `FUNCAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FUNCAO` (
  `CODIGO_FUNCAO` VARCHAR(2) NOT NULL,
  `NOME_FUNCAO` VARCHAR(40) NULL,
  PRIMARY KEY (`CODIGO_FUNCAO`));
""")

cur.execute("""
-- -----------------------------------------------------
-- Table `SUBFUNCAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SUBFUNCAO` (
  `CODIGO_SUBFUNCAO` VARCHAR(3) NOT NULL,
  `NOME_SUBFUNCAO` VARCHAR(40) NULL,
  `FUNCAO_CODIGO_FUNCAO` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`CODIGO_SUBFUNCAO`),
  CONSTRAINT `fk_SUBFUNCAO_FUNCAO1`
    FOREIGN KEY (`FUNCAO_CODIGO_FUNCAO`)
    REFERENCES `FUNCAO` (`CODIGO_FUNCAO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
""")

cur.execute("""
-- -----------------------------------------------------
-- Table `ACAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ACAO` (
  `CODIGO_ACAO` VARCHAR(4) NOT NULL,
  `NOME_ACAO` VARCHAR(40) NULL,
  `FONTE_FINALIDADE` VARCHAR(40) NULL,
  `PROGRAMA_CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
  `SUBFUNCAO_CODIGO_SUBFUNCAO` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`CODIGO_ACAO`, `PROGRAMA_CODIGO_PROGRAMA`),
  CONSTRAINT `fk_ACAO_PROGRAMA1`
    FOREIGN KEY (`PROGRAMA_CODIGO_PROGRAMA`)
    REFERENCES `PROGRAMA` (`CODIGO_PROGRAMA`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ACAO_SUBFUNCAO1`
    FOREIGN KEY (`SUBFUNCAO_CODIGO_SUBFUNCAO`)
    REFERENCES `SUBFUNCAO` (`CODIGO_SUBFUNCAO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
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
        NOME_FAVORECIDO VARCHAR(40) NOT NULL,
        FONTE_FINALIDADE VARCHAR(40),
        VALOR_PARCELA VARCHAR(8),
        MES_COMPETENCIA VARCHAR(10)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS FUNCAO_SUBFUNCAO (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CODIGO_FUNCAO VARCHAR(2) NOT NULL,
        NOME_FUNCAO VARCHAR(40),
        CODIGO_SUBFUNCAO VARCHAR(3) NOT NULL,
        NOME_SUBFUNCAO VARCHAR(40)
);
""")

cur.execute("""
    CREATE UNIQUE INDEX `siafi_UNIQUE` ON `MUNICIPIO` (`CODIGO_SIAFI_MUNICIPIO` ASC);
""")
cur.execute("""
        CREATE UNIQUE INDEX `NIS_FAVORECIDO_UNIQUE` ON `FAVORECIDO` (`NIS_FAVORECIDO` ASC);
""")
cur.execute("""
        CREATE INDEX `fk_FAVORECIDO_MUNICIPIO_idx` ON `FAVORECIDO` (`MUNICIPIO_CODIGO_SIAFI_MUNICIPIO` ASC);
""")
cur.execute("""
    CREATE INDEX `fk_PROGRAMA_has_FAVORECIDO_FAVORECIDO1_idx` ON `PAGAMENTO` (`FAVORECIDO_NIS_FAVORECIDO` ASC);
""")
cur.execute("""
    CREATE INDEX `fk_PROGRAMA_has_FAVORECIDO_PROGRAMA1_idx` ON `PAGAMENTO` (`PROGRAMA_CODIGO_PROGRAMA` ASC);
""")
cur.execute("""
    CREATE INDEX `fk_ACAO_PROGRAMA1_idx` ON `ACAO` (`PROGRAMA_CODIGO_PROGRAMA` ASC);
""")
cur.execute("""
    CREATE INDEX `fk_ACAO_SUBFUNCAO1_idx` ON `ACAO` (`SUBFUNCAO_CODIGO_SUBFUNCAO` ASC);
""")
cur.execute("""
    CREATE INDEX `fk_SUBFUNCAO_FUNCAO1_idx` ON `SUBFUNCAO` (`FUNCAO_CODIGO_FUNCAO` ASC);
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
