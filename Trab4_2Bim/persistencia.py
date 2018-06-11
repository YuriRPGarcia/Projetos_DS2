import psycopg2
from modelo import *

class Conexao:
	def abre(self):
		self.conexao = psycopg2.connect("dbname=COREinho user=postgres password=postgres host=localhost")
		self.cursor = self.conexao.cursor()

	def encerra(self):
		self.conexao.close()
		self.cursor.close()

class AlunoDAO:

	def adicionar(self, aluno):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [aluno.matricula, aluno.nome, aluno.senha, aluno.foto]
		conexaoObj.cursor.execute("INSERT INTO Aluno (matricula, nome, senha, foto) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Aluno")
		vet = conexao.cursor.fetchall()
		vetAluno = []
		for a in vet:
			vetAluno.append(Aluno(a[0], a[1], a[2], a[3]))
		conexao.encerra()
		return vetAluno	

	def editar(self, aluno):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [aluno.nome, aluno.senha, aluno.foto, aluno.matricula]
		conexaoObj.cursor.execute("UPDATE Aluno SET nome = %s, senha = %s, foto = %s WHERE matricula = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, matricula):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Aluno WHERE matricula = %s", [matricula])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, matricula):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Aluno WHERE matricula = %s", [matricula])
		a = conexao.cursor.fetchone()
		aluno = Aluno(a[0], a[1], a[2], a[3])
		conexao.encerra()
		return aluno

class EmpresaDAO:

	def adicionar(self, empresa):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [empresa.cnpj, empresa.nome, empresa.logo, empresa.senha]
		conexaoObj.cursor.execute("INSERT INTO Empresa (cnpj, nome, logo, senha) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Empresa")
		vet = conexao.cursor.fetchall()
		vetEmpresa = []
		for a in vet:
			vetEmpresa.append(Empresa(a[0], a[1], a[2], a[3]))
		conexao.encerra()
		return vetEmpresa	

	def editar(self, empresa):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [empresa.nome, empresa.logo, empresa.senha, empresa.cnpj]
		conexaoObj.cursor.execute("UPDATE Empresa SET nome = %s, logo = %s, senha = %s WHERE cnpj = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, cnpj):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Empresa WHERE cnpj = %s", [cnpj])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, cnpj):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Empresa WHERE cnpj = %s", [cnpj])
		a = conexao.cursor.fetchone()
		empresa = Empresa(a[0], a[1], a[2], a[3])
		conexao.encerra()
		return empresa

class EstagioDAO:

	def adicionar(self, estagio):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [estagio.empresa.cnpj, estagio.aluno.matricula, estagio.dataInicio, estagio.dataFim]
		conexaoObj.cursor.execute("INSERT INTO Estagio (cnpj, matricula, dataInicio, dataFim) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Estagio;")
		vet = conexao.cursor.fetchall()
		vetEstagio = []
		for a in vet:
			try:
				empresa = EmpresaDAO().obter(a[1])
			except TypeError:
				empresa = Empresa()
			try:
				aluno = AlunoDAO().obter(a[2])
			except TypeError:
				aluno = Aluno()
			vetEstagio.append(Estagio(a[0], empresa, aluno, a[3], a[4]))
		conexao.encerra()
		return vetEstagio

	def listar_porAluno(self, matricula):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Estagio WHERE matricula = %s;", [matricula])
		vet = conexao.cursor.fetchall()
		vetEstagio = []
		for a in vet:
			try:
				empresa = EmpresaDAO().obter(a[1])
			except TypeError:
				empresa = Empresa()
			aluno = AlunoDAO().obter(a[2])
			vetEstagio.append(Estagio(a[0], empresa, aluno, a[3], a[4]))
		conexao.encerra()
		return vetEstagio	

	def listar_porEmpresa(self, cnpj):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Estagio WHERE cnpj = %s;", [cnpj])
		vet = conexao.cursor.fetchall()
		vetEstagio = []
		for a in vet:
			empresa = EmpresaDAO().obter(a[1])
			try:
				aluno = AlunoDAO().obter(a[2])
			except TypeError:
				aluno = Aluno()
			vetEstagio.append(Estagio(a[0], empresa, aluno, a[3], a[4]))
		conexao.encerra()
		return vetEstagio	

	def editar(self, estagio):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [estagio.dataInicio, estagio.dataFim, estagio.cod]
		conexaoObj.cursor.execute("UPDATE Estagio SET dataInicio = %s, dataFim = %s WHERE cod = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, cod):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Estagio WHERE cod = %s", [cod])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, cod):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Estagio WHERE cod = %s", [cod])
		a = conexao.cursor.fetchone()
		try:
			empresa = EmpresaDAO().obter(a[1])
		except TypeError:
			empresa = Empresa()
		try:
			aluno = AlunoDAO().obter(a[2])
		except TypeError:
			aluno = Aluno()
		estagio = Estagio(a[0], empresa, aluno, a[3], a[4])
		conexao.encerra()
		return estagio