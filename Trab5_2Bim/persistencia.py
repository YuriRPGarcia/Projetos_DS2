import psycopg2
from modelo import *

class Conexao:
	
	def abre(self):
		self.conexao = psycopg2.connect("dbname= user=postgres password=postgres host=localhost")
		self.cursor = self.conexao.cursor()

	def encerra(self):
		self.conexao.close()
		self.cursor.close()

class AssuntoDAO:
	
	def adicionar(self, assunto):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("INSERT INTO Assunto (nome) VALUES(%s);", [assunto.nome])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Assunto")
		vet = conexao.cursor.fetchall()
		vetAssunto = []
		for a in vet:
			vetAssunto.append(Assunto(a[1], a[0]))
		conexao.encerra()
		return vetAssunto

	def editar(self, assunto):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("UPDATE Assunto SET nome = %s WHERE id = %s;", [assunto.nome, assunto.id])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, id):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Assunto WHERE id = %s", [id])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, id):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Assunto WHERE id = %s", [id])
		a = conexao.cursor.fetchone()
		assunto = Assunto(a[1], a[0])
		conexao.encerra()
		return assunto

class NoticiaDAO:

	def adicionar(self, noticia):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [noticia.titulo, noticia.texto, noticia.data, noticia.assunto.id]
		conexaoObj.cursor.execute("INSERT INTO Noticia (titulo, texto, data, idAssunto) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Noticia")
		vet = conexao.cursor.fetchall()
		vetNoticia = []
		for a in vet:
			try:
				assunto = AssuntoDAO().obter(a[3])
			except TypeError:
				assunto = Assunto()
			vetNoticia.append(Noticia(a[4], a[0], a[1], a[2], assunto))
		conexao.encerra()
		return vetNoticia

	def editar(self, noticia):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [noticia.titulo, noticia.texto, noticia.data, noticia.assunto.id, noticia.id]
		conexaoObj.cursor.execute("UPDATE Noticia SET titulo = %s, texto = %s, data = %s, idAssunto = %s WHERE id = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, id):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Noticia WHERE id = %s", [id])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, id):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Noticia WHERE id = %s", [id])
		try:
			assunto = AssuntoDAO().obter(a[3])
		except TypeError:
			assunto = Assunto()
		noticia = Noticia(a[4], a[0], a[1], a[2], assunto)
		conexao.encerra()
		return noticia

class Comentario:

	def adicionar(self, comentario):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [comentario.texto, comentario.data, comentario.noticia.id, comentario.leitor.id]
		conexaoObj.cursor.execute("INSERT INTO Comentario (texto, data, idNoticia, idLeitor) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Comentario")
		vet = conexao.cursor.fetchall()
		vetNoticia = []
		for a in vet:
			try:
				noticia = NoticiaDAO().obter(a[2])
			except TypeError:
				noticia = Noticia()
			try:
				leitor = LeitorDAO().obter(a[3])
			except TypeError:
				leitor = Leitor()
			vetNoticia.append(Noticia(a[4], a[0], a[1], noticia, leitor))
		conexao.encerra()
		return vetNoticia

	def editar(self, comentario):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [comentario.texto, comentario.data, comentario.id]
		conexaoObj.cursor.execute("UPDATE Comentario SET texto = %s, data = %s WHERE id = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, id):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Comentario WHERE id = %s", [id])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, id):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Comentario WHERE id = %s", [id])
		a = conexao.cursor.fetchone()
		try:
			noticia = NoticiaDAO().obter(a[2])
		except TypeError:
			noticia = Noticia()
		try:
			leitor = LeitorDAO().obter(a[3])
		except TypeError:
			leitor = Leitor()
		noticia = Comentario(a[4], a[0], a[1], noticia, leitor)
		conexao.encerra()
		return noticia