CREATE TABLE Email(
	Email VARCHAR(100) UNIQUE
);

CREATE TABLE Assunto(
	id SERIAL,
	nome VARCHAR(100),
	CONSTRAINT AssuntoPK PRIMARY KEY (id)
);

CREATE TABLE Pessoa(
	login VARCHAR(100),
	senha VARCHAR(100),
	nome VARCHAR(100),
	tipo VARCHAR(10),
	CONSTRAINT PessoaPK PRIMARY KEY (login)
);

CREATE TABLE Noticia(
	id SERIAL,
	titulo VARCHAR(1000),
	texto VARCHAR(10000),
	data DATE,
	foto VARCHAR(100),
	idAssunto INTEGER,
	CONSTRAINT NoticiaPK PRIMARY KEY (id),
	CONSTRAINT Noticia_AssuntoFK FOREIGN KEY (idAssunto) REFERENCES Assunto (id)
											ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Comentario(
	id SERIAL,
	texto VARCHAR(1000),
	data DATE,
	idNoticia INTEGER, 
	loginPessoa VARCHAR(100),
	CONSTRAINT ComentarioPK PRIMARY KEY (id),
	CONSTRAINT Comentario_NoticiaFK FOREIGN KEY (idNoticia) REFERENCES Noticia (id)
										   ON DELETE SET NULL ON UPDATE CASCADE,
	CONSTRAINT Comentario_LeitorFK FOREIGN KEY (loginPessoa) REFERENCES Pessoa (login)
											ON DELETE SET NULL ON UPDATE CASCADE
);




