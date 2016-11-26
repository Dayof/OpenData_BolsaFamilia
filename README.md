Dados Abertos - Bolsa Família
=============

Projeto que coleta dados abertos sobre o bolsa família e realiza CRUD e algumas outras operações sobre os dados de um determinado mês/ano.

### Ferramentas utilizadas

- Python 3
- SQLite3

### Features:
- Importar dados csv para db.

### TODO:
- DER,
- MR,
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

O script [import.sh](import.sh) executa o script [pre_import.sh](pre_import.sh) e os arquivos py [import_bf_csv.py](import_bf_csv.py) e [import_func_csv.py](import_func_csv.py) de acordo com a necessidade.

O script [pre_import.sh](pre_import.sh) trata os arquivos csvs da seguinte forma:
- Renomeia os arquivos extraído para o nome utilizado no arquivo py
- Elimina os headers dos csvs
- Inclui headers corretos nos csvs

O programa [import_bf_csv.py](import_bf_csv.py) irá importar os dados contidos no arquivo bf.csv usando o SQLite3 criando um arquivo do tipo db para manipular os dados importados.

O programa [import_func_csv.py](import_func_csv.py) irá importar os dados contidos no arquivo func_2015.csv usando o SQLite3 criando um arquivo do tipo db para manipular os dados importados.

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

Obs.: Os arquivos csv e db do bolsa família são muito extensos para incluí-los em um repositório Git, logo, deixe estes arquivos locais em sua máquina. O arquivo csv é baixado e o arquivo db é gerado.

### Checar BD

O comando a seguir imprime em terminal todos os dados que estavam contidos no arquivo csv.

``` bash
$ sqlite3 bf.db 'select * from FAVORECIDOS'
$ sqlite3 func_2015.db 'select * from FUNCAO'
```

### Motivação

Projeto final da matéria de Banco de Dados, professora Maristela.
Universidade de Brasília (UnB), 2016/2.

### Autoria
Dayanne Fernandes da Cunha - 13/0107191 <br>
Christian Costa Werner - 14/0134573
