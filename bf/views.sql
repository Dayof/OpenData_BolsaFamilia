-- TRANSACTION para inserir view de consulta dos favorecidos que ganham mais do PBF
BEGIN TRANSACTION;

DROP VIEW MAIS_FAVORECIDOS;

CREATE VIEW MAIS_FAVORECIDOS
AS
SELECT
    f.nis_favorecido as nis,
    f.nome_favorecido as nome,
    p.valor_parcela as valor,
    p.mes_competencia as mes
FROM FAVORECIDO f
JOIN PAGAMENTO p ON nis=p.favorecido_nis_favorecido
ORDER BY p.valor_parcela DESC;

COMMIT;
