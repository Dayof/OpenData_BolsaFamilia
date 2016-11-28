Dados Abertos - Bolsa Família
=============

Projeto que coleta dados abertos sobre o bolsa família e realiza CRUD e algumas outras operações sobre os dados de um determinado mês/ano.

### Ferramentas utilizadas

- Python 3
- Virtualenv
- Pip
- Flask
- Bash Script
- SQLite 3
- MySQL Workbench

### Features:
- Importar dados csv para db,
- DER,
- MR.

### TODO:
- Camadas de Apresentação,
- Camada de Negócio,
- Camada de Persistência.

### Dados utilizados

- Bolsa Família : Pagamentos

Dados de pagamentos da despesa do programa social "Bolsa Família" da data de Setembro/2015.

O arquivo csv dos dados abertos pode ser encontrado neste [link](http://www.portaltransparencia.gov.br/downloads/mensal.asp?c=BolsaFamiliaFolhaPagamento#exercicios2015).

- Despesas : Classificação Funcional da Despesa (MTO)

Informações, em formato aberto, da classificação funcional da Despesa, publicada no Manual Técnico de Orçamento, pelo Ministério do Planejamento, do ano de 2015.

O arquivo csv dos dados abertos pode ser encontrado neste [link](http://www.portaldatransparencia.gov.br/downloads/anual.asp?c=Funcoes#exercicios2015).

### Importar Dados (CSV)

O script [import.sh](import.sh) executa o script [pre_import.sh](pre_import.sh) e o arquivos py [import_bf_csv.py](import_bf_csv.py) de acordo com a necessidade.

O script [pre_import.sh](pre_import.sh) trata os arquivos csvs da seguinte forma:
- Renomeia os arquivos extraído para o nome utilizado no arquivo py
- Elimina os headers dos csvs
- Inclui headers corretos nos csvs

O programa [import_bf_csv.py](import_bf_csv.py) irá importar os dados contidos no arquivo bf.csv e func_2015.csv usando o SQLite3 criando um arquivo do tipo db para manipular os dados importados. Ele também cria as tabelas primárias para importar os dados do CSV e também as tabelas normalizadas a nível 3F.

AVISO: A execução a seguir pode levar um tempo, pois irá processar aproximadamente 2gb de dados.

Passos a executar:

1. Download do arquivo csv do bolsa família de 09/2015 e funções de 2015;
2. Colocar na pasta raiz;
3. Extrair os arquivos;
4. Executar o script [import.sh](import.sh) para tratar os arquivos csvs e importar os csvs para os dbs.

Executando o script [import.sh](import.sh):

``` bash
$ bash import.sh
```

Obs.: Os arquivos csv e db são muito extensos para incluí-los em um repositório Git, logo, deixe estes arquivos locais em sua máquina. O arquivo csv é baixado e o arquivo db é gerado.

### Checar BD

O comando a seguir imprime em terminal todos os dados que estavam contidos no arquivo csv.

``` bash
$ sqlite3 bf.db 'select * from BOLSA_FAMILIA'
$ sqlite3 bf.db 'select * from FUNCAO_SUBFUNCAO'
```

### Tabelas 3F

Na pasta [MR](MR) temos o diagrama, modelo e script SQL das tabelas normalizadas na forma 3F geradas a partir do MySQL Workbench, para verificar o esquema das tabelas é só utilizar o SQLite3 executando os seguintes comandos:

``` bash
$ cd MR
$ sqlite3
$ sqlite> .read EER.sql
```

Para inserir os dados abertos nas tabelas normalizadas em 3F é só executar o script SQL [normalize.sql](normalize.sql):

``` bash
$ sqlite3 bf.db < normalize.sql
```

### Web Service

Utilizando o Python 3 e o framework web Flask foram implementadas camadas de persistência e apresentação para possibilitar o CRUD do sistema e as consultas no banco de dados.

- Criar environment do sistema:

``` bash
$ virtualenv env
```

- Para instalar o Flask e continuar a desenvolver:

``` bash
$ . env/bin/activate
$ export BF_SETTINGS=config.py
$ pip install --editable .
$ export FLASK_APP=bf
```

- Para iniciar o Web Service:

``` bash
$ flask run
```

A aplicação estará ativa no endereço http://localhost:5000/ .

- Para sair do environment:

``` bash
$ deactivate
```

### Relatório

Na pasta [doc](doc) contém o relatório do projeto com o passo a passo de desenvolvimento, desde a análise de cada campo nas tabelas até o desenvolvimento da GUI.

### Motivação

Projeto final da matéria de Banco de Dados, professora Maristela.
Universidade de Brasília (UnB), 2016/2.

### Autoria
Dayanne Fernandes da Cunha - 13/0107191 <br>
Christian Costa Werner - 14/0134573
