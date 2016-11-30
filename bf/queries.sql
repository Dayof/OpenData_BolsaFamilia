-- Seleciona todos as ordens de pagamento na base de dados
SELECT
    NIS_FAVORECIDO AS nis,
    MES_COMPETENCIA as mes,
    VALOR_PARCELA as valor
FROM
    PAGAMENTO;

-- Seleciona todos os favorecidos na base de dados em ordem alfabetica
SELECT
    NOME_FAVORECIDO AS nis,
    CODIGO_SIAFI_MUNICIPIO AS nome
FROM
    FAVORECIDO
ORDER BY nome ASC;

-- Ordena os estados em ordem maior beneficiado pelo programa bolsa familia
SELECT
    m.uf AS estado,
    SUM(p.valor_parcela) AS total
FROM
    MUNICIPIO m
LEFT JOIN FAVORECIDO f ON f.CODIGO_SIAFI_MUNICIPIO = m.CODIGO_SIAFI_MUNICIPIO
JOIN PAGAMENTO p ON f.nis_favorecido = p.nis_favorecido
GROUP BY
    estado;

-- Total de favorecidos por estado
SELECT
    m.uf as estado,
    COUNT(p.codigo_siafi_municipio) AS total_fav
FROM
    MUNICIPIO m
LEFT JOIN FAVORECIDO f ON m.codigo_siafi_municipio = f.codigo_siafi_municipio
GROUP BY
    estado
ORDER BY
    total_fav;

-- Media de pagamentos
SELECT
    AVG(valor_parcela) AS med_pag
FROM
    PAGAMENTO;

-- Media de pagamentos por estado
SELECT
    m.uf AS estado,
    AVG(p.valor_parcela) AS med_state
FROM
    MUNICIPIO m
LEFT JOIN FAVORECIDO f ON m.codigo_siafi_municipio = f.codigo_siafi_municipio
LEFT JOIN PAGAMENTO p ON f.nis_favorecido = p.nis_favorecido
GROUP BY
    estado
ORDER BY
    med_state;
