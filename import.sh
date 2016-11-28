#!bin/bash
DIR_BF=bf
BF_DB="DIR_BF/bf.db"

error()
{
	echo "################ ERROR BEFORE FINISHING THE SCRIPT ################"
	exit
}

echo "Pré-processamento das tabelas iniciado..."
bash pre_import.sh || error

if [ -f "$BF_DB" ]; then
    echo "Database do bolsa família e funções já foram processados!"
else
    echo "Processando database da bolsa família e das funções..."
    python3 import_bf_csv.py || error
	mv bf.db bf/
fi
