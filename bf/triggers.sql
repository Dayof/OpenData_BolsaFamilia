-- TRIGGER para deletar ordens de pagamento de um favorecido que não existirá mas na base de dados
BEGIN TRANSACTION;

DROP TRIGGER DELETE_FAVORECIDO;

CREATE TRIGGER DELETE_FAVORECIDO
AFTER DELETE ON FAVORECIDO
FOR EACH ROW
BEGIN
    DELETE FROM
        PAGAMENTO p
    WHERE
        p.nis_favorecido = OLD.nis_favorecido
END;

COMMIT;
