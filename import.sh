#!bin/bash
DIR_BF=bf
BF_DB="DIR_BF/parcial.db"

error()
{
	echo "################ ERROR BEFORE FINISHING THE SCRIPT ################"
	exit
}

echo "Pré-processamento das tabelas iniciado..."
bash pre_import.sh || error

if [ -f "$BF_DB" ]
then
    echo "Database do bolsa família e funções já foram processados!"
else
    echo "Processando database da bolsa família e das funções..."
    python3 import_bf_csv.py || error
	echo "Populando database das tabelas normalizadas..."
    python3 pop.py || error
	mv parcial.db bf/ || error
	cd "$DIR_BF" || error
	sqlite3 parcial.db < views.sql || error
fi
