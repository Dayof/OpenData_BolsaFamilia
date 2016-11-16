mv "201509_BolsaFamiliaFolhaPagamento.csv" "bf2.csv"
sed '1d' bf2.csv > bf.csv
sed -i '' $'1i\
UF\\\tCODIGO_SIAFI_MUNICIPIO\\\tNOME_MUNICIPIO\\\tCODIGO_FUNCAO\\\tCODIGO_SUBFUNCAO\\\tCODIGO_PROGRAMA\\\tCODIGO_ACAO\\\tNIS_FAVORECIDO\\\tNOME_FAVORECIDO FONTE_FINALIDADE\\\tVALOR_PARCELA\\\tMES_COMPETENCIA
' bf.csv
rm bf2.csv
