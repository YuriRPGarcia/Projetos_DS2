CREATE TABLE Filme(
	cod SERIAL,
	titulo VARCHAR(100),	
	sinopse VARCHAR(500),
	genero VARCHAR(50),
	foto VARCHAR(100),
	dataInicio DATE,
	dataFim DATE,
	CONSTRAINT FilmePK PRIMARY KEY (cod)
);

CREATE TABLE Sessao(
	cod SERIAL,
	dia DATE,
	hora TIME,
	codFilme INTEGER,
	CONSTRAINT SessaoPK PRIMARY KEY (cod),
	CONSTRAINT Sessao_FilmePK FOREIGN KEY (codFilme) REFERENCES Filme (cod)
									    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Ingresso(
	cod SERIAL,
	nomeCliente VARCHAR(100),
	cadeira INTEGER,
	codSessao INTEGER,
	CONSTRAINT IngressoPK PRIMARY KEY (cod),
	CONSTRAINT Ingresso_SessaoFK FOREIGN KEY (codSessao) REFERENCES Sessao (cod)
											 ON UPDATE CASCADE ON DELETE CASCADE
);