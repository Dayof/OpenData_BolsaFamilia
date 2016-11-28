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
SELECT uf AS Estado, SUM(valor_parcela) AS Total
FROM municipio
LEFT JOIN favorecido ON nome_municipio = municipio_nome_municipio
JOIN pagamento ON nis_favorecido = favorecido_nis_favorecido
GROUP BY Estado;


