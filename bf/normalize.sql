DROP TABLE IF EXISTS `MUNICIPIO` ;
DROP TABLE IF EXISTS `PROGRAMA` ;
DROP TABLE IF EXISTS `FUNCAO` ;
DROP TABLE IF EXISTS `SUBFUNCAO` ;
DROP TABLE IF EXISTS `ACAO` ;

-- -----------------------------------------------------
-- Table `MUNICIPIO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MUNICIPIO` (
    `CODIGO_SIAFI_MUNICIPIO` VARCHAR(4) NOT NULL,
    `NOME_MUNICIPIO` VARCHAR(15) NULL,
    `UF` VARCHAR(2) NULL,
    PRIMARY KEY (`CODIGO_SIAFI_MUNICIPIO`));

-- -----------------------------------------------------
-- Table `PROGRAMA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PROGRAMA` (
  `CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
  `NOME_PROGRAMA` VARCHAR(50) NULL,
  PRIMARY KEY (`CODIGO_PROGRAMA`));

-- -----------------------------------------------------
-- Table `FUNCAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FUNCAO` (
  `CODIGO_FUNCAO` VARCHAR(2) NOT NULL,
  `NOME_FUNCAO` VARCHAR(50) NULL,
  PRIMARY KEY (`CODIGO_FUNCAO`));

-- -----------------------------------------------------
-- Table `SUBFUNCAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SUBFUNCAO` (
  `CODIGO_SUBFUNCAO` VARCHAR(3) NOT NULL,
  `NOME_SUBFUNCAO` VARCHAR(50) NULL,
  `CODIGO_FUNCAO` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`CODIGO_SUBFUNCAO`));

-- -----------------------------------------------------
-- Table `ACAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ACAO` (
  `CODIGO_ACAO` VARCHAR(4) NOT NULL,
  `NOME_ACAO` VARCHAR(100) NULL,
  `FONTE_FINALIDADE` VARCHAR(50) NULL,
  `CODIGO_PROGRAMA` VARCHAR(4) NOT NULL,
  `CODIGO_SUBFUNCAO` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`CODIGO_ACAO`, `CODIGO_PROGRAMA`));

insert into FUNCAO (CODIGO_FUNCAO, NOME_FUNCAO)
    select distinct fsf.CODIGO_FUNCAO, fsf.NOME_FUNCAO
    from FUNCAO_SUBFUNCAO as fsf
    where fsf.CODIGO_FUNCAO is not null;

insert into SUBFUNCAO (CODIGO_SUBFUNCAO, NOME_SUBFUNCAO, CODIGO_FUNCAO)
    select fsf.CODIGO_SUBFUNCAO, fsf.NOME_SUBFUNCAO, fsf.CODIGO_FUNCAO
    from FUNCAO_SUBFUNCAO as fsf
    where fsf.CODIGO_SUBFUNCAO is not null
    and fsf.CODIGO_FUNCAO is not null;

insert into MUNICIPIO (CODIGO_SIAFI_MUNICIPIO, NOME_MUNICIPIO, UF)
    select distinct bf.CODIGO_SIAFI_MUNICIPIO, bf.NOME_MUNICIPIO, bf.UF
    from BOLSA_FAMILIA as bf
    where bf.CODIGO_SIAFI_MUNICIPIO is not null;

insert into PROGRAMA (CODIGO_PROGRAMA, NOME_PROGRAMA) values
    ("1335", "Transferência de Renda com Condicionalidades");

insert into ACAO (CODIGO_ACAO, NOME_ACAO, FONTE_FINALIDADE, CODIGO_PROGRAMA, CODIGO_SUBFUNCAO) values
    ("8442", "Transferência de Renda Diretamente às Famílias em Condição de Pobreza e Extrema Pobreza", "CAIXA - Programa Bolsa Família", "1335", "244");
