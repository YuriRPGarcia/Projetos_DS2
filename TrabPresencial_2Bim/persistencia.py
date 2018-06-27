import psycopg2
from modelo import *

class Conexao:
	
	def abre(self):
		self.conexao = psycopg2.connect("dbname=Anotacoes user=postgres password=postgres host=localhost")
		self.cursor = self.conexao.cursor()

	def encerra(self):
		self.conexao.close()
		self.cursor.close()

class AnotacaoDAO:
	
	def adicionar(self, anotacao):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [anotacao.titulo, anotacao.texto, anotacao.foto]
		conexaoObj.cursor.execute("INSERT INTO Anotacao (titulo, texto, foto) VALUES(%s, %s, %s) RETURNING id;", dados)
		conexaoObj.conexao.commit()
		id = conexaoObj.cursor.fetchone()[0]
		conexaoObj.encerra()
		return int(id)

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Anotacao")
		vet = conexao.cursor.fetchall()
		vetAnotacoes = []
		for a in vet:
			vetAnotacoes.append(Anotacao(a[1], a[2], a[3], a[0]))
		conexao.encerra()
		return vetAnotacoes

	def editar(self, anotacao):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [anotacao.titulo, anotacao.texto, anotacao.foto, anotacao.id]
		conexaoObj.cursor.execute("UPDATE Anotacao SET titulo = %s, texto = %s, foto = %s WHERE id = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, id):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Anotacao WHERE id = %s", [id])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, id):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Anotacao WHERE id = %s", [id])
		a = conexao.cursor.fetchone()
		anotacao = Anotacao(a[1], a[2], a[3], a[0])
		conexao.encerra()
		return anotacao