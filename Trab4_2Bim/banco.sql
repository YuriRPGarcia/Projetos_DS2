CREATE TABLE Aluno(
	matricula VARCHAR(8),
	nome VARCHAR(100),
	senha VARCHAR(100),
	foto VARCHAR(100),
	CONSTRAINT AlunoPK PRIMARY KEY (matricula)
);

CREATE TABLE Empresa(
	cnpj VARCHAR(14),
	nome VARCHAR(100),
	logo VARCHAR(100),
	senha VARCHAR(100),
	CONSTRAINT EmpresaPK PRIMARY KEY (cnpj)
);

CREATE TABLE Estagio(
	cod SERIAL,
	cnpj VARCHAR(14),
	matricula VARCHAR(8),
	dataInicio DATE, 
	dataFim DATE,
	CONSTRAINT EstagioPK PRIMARY KEY (cod),
	CONSTRAINT Estagio_EmpresaFK FOREIGN KEY (cnpj) REFERENCES Empresa (cnpj)
							 ON DELETE SET NULL ON UPDATE CASCADE,
	CONSTRAINT Estagio_AlunoFK FOREIGN KEY (matricula) REFERENCES Aluno (matricula)
								   ON DELETE SET NULL ON UPDATE CASCADE
);