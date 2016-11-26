#!bin/bash
BF_FILE=bf.csv
FUNC_FILE=func_2015.csv

error()
{
	echo "################ ERROR BEFORE FINISHING THE SCRIPT ################"
	exit
}

if [ -f "$BF_FILE" ]; then
    echo "CSV do bolsa família já foi processado."
else
    echo "Processando CSV da bolsa família..."
    mv "201509_BolsaFamiliaFolhaPagamento.csv" "bf2.csv" || error
    sed '1d' bf2.csv > bf.csv
    sed -i '' $'1i\
    UF\\\tCODIGO_SIAFI_MUNICIPIO\\\tNOME_MUNICIPIO\\\tCODIGO_FUNCAO\\\tCODIGO_SUBFUNCAO\\\tCODIGO_PROGRAMA\\\tCODIGO_ACAO\\\tNIS_FAVORECIDO\\\tNOME_FAVORECIDO\\\tFONTE_FINALIDADE\\\tVALOR_PARCELA\\\tMES_COMPETENCIA
    ' bf.csv
    rm bf2.csv
fi

if [ -f "$FUNC_FILE" ]; then
    echo "CSV das classificações funcionais das despesas já foi processado."
else
    echo "Processando CSV das funções..."
    mv "2015_Funcoes.csv" "func.csv" || error
    sed '1d' func.csv > func_2015.csv
    sed -i '' $'1i\
    CODIGO_FUNCAO\\\tNOME_FUNCAO\\\tCODIGO_SUBFUNCAO\\\tNOME_SUBFUNCAO
    ' func_2015.csv
    rm func.csv
fi
