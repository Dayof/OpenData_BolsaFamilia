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

Dados de pagamentos da despesa do programa social "Bolsa Família" da data de Setembro/2015.

O arquivo csv dos dados abertos pode ser encontrado neste [link](http://www.portaltransparencia.gov.br/downloads/mensal.asp?c=BolsaFamiliaFolhaPagamento#exercicios2015).

### Importar Dados (CSV)

O script [pre_import.sh](pre_import.sh) trata o arquivo csv da seguinte forma:
- Renomeia o arquivo extraído para o nome utilizado no arquivo py
- Elimina header do csv
- Inclui header correto no csv

O programa [import_csv.py](import_csv.py) irá importar os dados contidos no arquivo csv usando o SQLite3 criando um arquivo do tipo db para manipular os dados importados.

AVISO: A execução a seguir pode levar um tempo, pois irá processar aproximadamente 2gb de dados.

Passos a executar:

1. Download do arquivo csv de 09/15
2. Colocar na pasta raiz
3. Extrair o arquivo
4. Executar o script para tratar o arquivo csv
5. Executar o arquivo py para importar o csv para db

Executar o script para tratar o arquivo csv:

``` bash
$ bash pre_import.sh
```

Executar o arquivo py para importar o csv para db:

``` bash
$ python import_csv.py
```

Obs.: Os arquios csv e db são muito extensos para incluí-los em um repositório Git, logo, deixe estes arquivos locais em sua máquina. O arquivo csv é baixado e o arquivo db é gerado.

### Checar BD

O comando a seguir imprime em terminal todos os dados que estavam contidos no arquivo csv.

``` bash
$ sqlite3 bf.db 'select * from FAVORECIDOS'
```

### Motivação

Projeto final da matéria de Banco de Dados, professora Maristela.
Universidade de Brasília (UnB), 2016/2.

### Autoria
Dayanne Fernandes da Cunha - 13/0107191
Christian Costa Werner - 14/0134573
