create database API;
use API;

-- -----------------------------------------------------
-- Table chamados
-- -----------------------------------------------------

create table chamados(
	id_chamado int not null primary key auto_increment,
	data_de_inicio timestamp,
	data_de_termino timestamp,
-- usuario
    nome_usuario varchar(40),
    email_usuario VARCHAR(45),
    id_usuario int, -- FK USUARIO
    telefone_usuario varchar (11),
    assunto varchar (50), -- tipo problema
    descricao varchar (850),
-- executor
	id_executor int, -- FK EXECUTOR
	resposta_chamado varchar(850),
    aceitar_chamado BINARY(1)
);

-- -----------------------------------------------------
-- Table usuario
-- -----------------------------------------------------

create table usuario (
	id_usuario int not null primary key auto_increment,
	cpf_usuario varchar (11),
    id_chamado int,
    Foreign Key(id_chamado) references chamados(id_chamado)
);
-- -----------------------------------------------------
-- Table executor
-- -----------------------------------------------------

create table executor(
	id_executor int not null primary key auto_increment,
	cpf_executor varchar (11),
	id_chamado int,
    Foreign Key(id_chamado) references chamados(id_chamado)
);

-- FK ids
ALTER TABLE chamados ADD 
foreign KEY (id_usuario) 
REFERENCES usuario (id_usuario);

ALTER TABLE chamados ADD 
foreign KEY (id_executor) 
REFERENCES executor (id_executor);


insert into usuario (cpf_usuario) values ('12345678912');
select * from usuario;

