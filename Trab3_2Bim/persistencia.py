import psycopg2
from modelo import *

class Conexao:
	def abre(self):
		self.conexao = psycopg2.connect("dbname=cinema user=postgres password=postgres host=localhost")
		self.cursor = self.conexao.cursor()

	def encerra(self):
		self.conexao.close()
		self.cursor.close()

class FilmeDAO:
	
	def adicionar(self, filme):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [filme.titulo, filme.sinopse, filme.genero, filme.dataInicio, filme.dataFim, filme.foto]
		conexaoObj.cursor.execute("INSERT INTO Filme (titulo, sinopse, genero, dataInicio, dataFim, foto) VALUES(%s, %s, %s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Filme")
		vet = conexao.cursor.fetchall()
		vetFilme = []
		for a in vet:
			vetFilme.append(Filme(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
		conexao.encerra()
		return vetFilme	

	def alterar(self, filme):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [filme.titulo, filme.sinopse, filme.genero, filme.dataInicio, filme.dataFim, filme.foto, filme.cod]
		conexaoObj.cursor.execute("UPDATE Filme SET titulo = %s, sinopse = %s, genero = %s, dataInicio = %s, dataFim = %s, foto = %s WHERE cod = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, cod):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Filme WHERE cod = %s", [cod])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, cod):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Filme WHERE cod = %s", [cod])
		a = conexao.cursor.fetchone()
		filme = Filme(a[0], a[1], a[2], a[3], a[4], a[5], a[6])
		conexao.encerra()
		return filme

class SessaoDAO:
	
	def adicionar(self, sessao):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [sessao.dia, sessao.hora, sessao.codFilme]
		conexaoObj.cursor.execute("INSERT INTO Sessao (dia, hora, codFilme) VALUES(%s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self, codFilme):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Sessao WHERE codFilme = %s", codFilme)
		vet = conexao.cursor.fetchall()
		vetSessao = []
		for a in vet:
			vetSessao.append(Sessao(a[0], a[1], a[2], a[3]))
		conexao.encerra()
		return vetSessao

	def alterar(self, sessao):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [sessao.dia, sessao.hora, sessao.codFilme, sessao.cod]
		conexaoObj.cursor.execute("UPDATE Sessao SET dia = %s, hora = %s, codFilme = %s WHERE cod = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def excluir(self, cod):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Sessao WHERE cod = %s", [cod])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, cod):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Sessao WHERE cod = %s", [cod])
		a = conexao.cursor.fetchone()
		sessao = Sessao(a[0], a[1], a[2], a[3])
		conexao.encerra()
		return sessao

class IngressoDAO:
	
	def adicionar(self, ingresso):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [ingresso.nomeCliente, ingresso.cadeira, ingresso.codSessao]	
		conexaoObj.cursor.execute("INSERT INTO Ingresso (nomeCliente, cadeira, codSessao) VALUES(%s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()	

	def listar(self, codSessao):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Ingresso WHERE codSessao = %s", codSessao)
		vet = conexao.cursor.fetchall()
		vetIngresso = []
		for a in vet:
			vetIngresso.append(Ingresso(a[0], a[1], a[2], a[2]))
		conexao.encerra()
		return vetIngresso

	def alterar(self, ingresso):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [ingresso.nomeCliente, ingresso.cadeira, ingresso.codSessao, ingresso.cod]
		conexaoObj.cursor.execute("UPDATE Ingresso SET nomeCliente = %s, cadeira = %s, codSessao = %s WHERE cod = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def excluir(self, cod):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Ingresso WHERE cod = %s", [cod])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, cod):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Ingresso WHERE cod = %s", [cod])
		a = conexao.cursor.fetchone()
		ingresso = Ingresso(a[0], a[1], a[2], a[3])
		conexao.encerra()
		return ingresso