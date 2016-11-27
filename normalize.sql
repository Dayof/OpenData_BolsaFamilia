insert into FUNCAO (CODIGO_FUNCAO, NOME_FUNCAO)
    select distinct fsf.CODIGO_FUNCAO, fsf.NOME_FUNCAO
    from FUNCAO_SUBFUNCAO as fsf
    where fsf.CODIGO_FUNCAO is not null;

insert into SUBFUNCAO (CODIGO_SUBFUNCAO, NOME_SUBFUNCAO, FUNCAO_CODIGO_FUNCAO)
    select fsf.CODIGO_SUBFUNCAO, fsf.NOME_SUBFUNCAO, fsf.CODIGO_FUNCAO
    from FUNCAO_SUBFUNCAO as fsf
    where fsf.CODIGO_SUBFUNCAO is not null
    and fsf.CODIGO_FUNCAO is not null;
