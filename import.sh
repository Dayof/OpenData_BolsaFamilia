#!bin/bash
BF_DB="bf.db"
FUNC_DB="func_2015.db"

echo "Pré-processamento das tabelas iniciado..."
bash pre_import.sh || exit

if [ -f "$BF_DB" ]; then
    echo "Database do bolsa família já foi processado!"
else
    echo "Processando database da bolsa família..."
    python3 import_bf_csv.py || exit
fi

if [ -f "$FUNC_DB" ]; then
    echo "Database das classificações funcionais das despesas já foi processado!"
else
    echo "Processando database das funções..."
    python3 import_func_csv.py || exit
fi
