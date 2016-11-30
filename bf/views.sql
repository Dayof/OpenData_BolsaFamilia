-- TRANSACTION para inserir view de consulta que ordena os favorecidos em ordem de maior pagamento na base de dados
BEGIN TRANSACTION;

CREATE VIEW IF NOT EXISTS MAIS_FAVORECIDOS
AS
SELECT
    f.nis_favorecido as nis,
    f.nome_favorecido as nome,
    sum(p.valor_parcela) as total,
    p.mes_competencia as mes
FROM
    FAVORECIDO f
INNER JOIN PAGAMENTO p ON nis=p.nis_favorecido
GROUP BY
    nis,
    nome,
    mes
ORDER BY p.valor_parcela DESC;

COMMIT;
