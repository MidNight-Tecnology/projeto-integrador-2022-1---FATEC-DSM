-- -----------------------------------------------------
-- Criação e Utilização de Banco de Dados
-- -----------------------------------------------------

Create Database API;
Use API;
-- drop database API;
-- -----------------------------------------------------
-- Tabela dos Chamados
-- -----------------------------------------------------

Create Table chamados(
-- Chamado	
    id_chamado Int Not Null Primary Key Auto_Increment, -- Id dos Chamados;
	data_de_inicio Datetime, -- Data de ínicio;
	data_de_termino Datetime, -- Data de Fechamento;
-- Cliente
    id_usuario Int, -- FK Usuários;
    nome_usuario Varchar(100),
    assunto Varchar(50), Check (assunto = 'Problema de Hardware' or assunto = 'Problema de Software' or assunto = 'Esclarecimento/Informação'), -- Tipos de problema;
    descricao Varchar(850), -- Descrição de Abertura;
	imaarq Longblob,
	avaliacao Int(2) Check (avaliacao = 10 or avaliacao = 9 or avaliacao = 8 or avaliacao = 7 or avaliacao = 6 or avaliacao = 5 or avaliacao = 4 or avaliacao = 3 or avaliacao = 2 or avaliacao = 1 or avaliacao = 0), -- Avaliação por Emote 😁😀😐😢😭;
     -- comentario da avaliaçao :)
-- Técnico
	id_usuario_resp Int, -- FK Usuários;
	resposta_chamado Varchar(850), -- Resposta do Chamado;
    estado_chamado Varchar(25) Check (estado_chamado = 'Finalizado'  or estado_chamado = 'Rejeitado' or estado_chamado = 'Processando'), -- Aceitação ou não de Serviço.
    nome_resposta Varchar(100),
    coment_aval varchar (100)
);

-- -----------------------------------------------------
-- Table dos Usuários
-- -----------------------------------------------------

Create Table usuarios (
	id_usuario Int Not Null Primary Key Auto_Increment, -- Id dos Usuários;
	nome Varchar(100), -- Nome dos Usuários;
    email Varchar(200) Unique, -- Email dos Usuários;
	senha Varchar(100), -- Senha dos Usuários;
    genero Char(1) Check (genero = 'F' or genero = 'M'), -- Gênero do Usuário;
    telefone Varchar(11), -- Telefone dos Usuários;
    classe Varchar(15) Check (classe = 'Administrador' or classe = 'Cliente' or classe = 'Técnico'), -- Classe dos Usuários;
    atividade Varchar(10) Check (atividade = 'Ativo' or atividade = 'Inativo'), -- Atividade do Usuário;
    contador Int Unique -- Contador ciclico
);

-- -----------------------------------------------------
-- Alterações de Tabela
-- -----------------------------------------------------

Alter Table chamados Add constraint fk_usu_cham
Foreign Key (id_usuario) 
References usuarios (id_usuario);

Alter Table chamados Add constraint fk_usu_cham_resp
Foreign Key (id_usuario_resp) 
References usuarios (id_usuario);

-- -----------------------------------------------------
-- Inserção e Seleção de Dados na Tabela
-- -----------------------------------------------------


Insert Into usuarios (nome, email, telefone, senha, classe, atividade) values ('ADM','adm@gmail.com',12996126985,'adm','Administrador','Ativo');

Select * From chamados;
Select * From usuarios;

-- -----------------------------------------------------
-- Conferindo as informações dos Dados das Tabelas
-- -----------------------------------------------------

desc chamados;

select * from information_schema.table_constraints
where table_name='chamados';

select * from information_schema.table_constraints
where table_name='usuarios';

-- -----------------------------------------------------
-- Deletando o Banco de Dados
-- -----------------------------------------------------

-- drop database API;
-- drop table chamados;

select * from chamados order by data_de_inicio desc;


 



