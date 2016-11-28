-- Seleciona todos os favorecidos na base de dados em ordem alfabetica
SELECT nis_favorecido AS NIS, nome_favorecido AS Nome
FROM favorecido
ORDER BY nome;

-- Ordena os favorecidos em ordem de maior pagamento na base de dados.
CREATE VIEW mais_favorecidos AS
SELECT nis_favorecido AS NIS, nome_favorecido as Nome, valor_parcela, mes_competencia
FROM favorecido f
JOIN pagamento ON nis = favorecido_nis_favorecido
ORDER BY valor_parcela DESC;

-- Ordena os estados em ordem maior beneficiado pelo programa bolsa familia
CREATE PROCEDURE uf_mais_favorecidos AS
BEGIN
SELECT uf AS Estado,
SUM(valor_parcela) AS Total
FROM municipio
LEFT JOIN favorecido
ON CODIGO_SIAFI_MUNICIPIO = MUNICIPIO_CODIGO_SIAFI_MUNICIPIO
JOIN pagamento
ON nis_favorecido = favorecido_nis_favorecido
GROUP BY Estado
END;

-- Total de favorecidos por estado
SELECT uf, COUNT(municipio_codigo_siafi_municipio) AS "Total favorecidos"
FROM municipio
LEFT JOIN favorecido ON codigo_siafi_municipio = municipio_codigo_siafi_municipio
GROUP BY uf
ORDER BY "Total favorecidos";

-- Media de pagamentos
SELECT AVG(valor_parcela) AS "Media de pagamento"
FROM pagamento;

-- Media de pagamentos por estado
SELECT uf, AVG(valor_parcela) AS "Media por estado"
FROM municipio
LEFT JOIN favorecido ON codigo_siafi_municipio = municipio_codigo_siafi_municipio
LEFT JOIN pagamento ON nis_favorecido = favorecido_nis_favorecido
GROUP BY uf
ORDER BY "Media por estado";
