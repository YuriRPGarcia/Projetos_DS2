import psycopg2
from modelo import *

class Conexao:
	
	def abre(self):
		self.conexao = psycopg2.connect("dbname=news user=postgres password=postgres host=localhost")
		self.cursor = self.conexao.cursor()

	def encerra(self):
		self.conexao.close()
		self.cursor.close()

class EmailDAO:
	
	def adicionar(self, email):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("INSERT INTO Email (email) VALUES(%s);", [email])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()
	
	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Email")
		vet = conexao.cursor.fetchall()
		vetEmails = []
		for a in vet:
			vetEmails.append(a[0])
		conexao.encerra()
		return vetEmails		

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

	def obterporNome(self, nome):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Assunto WHERE nome = %s", [nome])
		a = conexao.cursor.fetchone()
		assunto = Assunto(a[1], a[0])
		conexao.encerra()
		return assunto

class PessoaDAO:

	def adicionar(self, pessoa):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [pessoa.tipo, pessoa.login, pessoa.senha, pessoa.nome]
		conexaoObj.cursor.execute("INSERT INTO Pessoa (tipo, login, senha, nome) VALUES(%s, %s, MD5(%s), %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self, tipo):
		if(tipo == "todos"):
			conexao = Conexao()
			conexao.abre()
			conexao.cursor.execute("SELECT * FROM Pessoa WHERE tipo = %s")
			vet = conexao.cursor.fetchall()
			vetPessoa = []
			for a in vet:
				vetPessoa.append(Pessoa(a[3], a[0], a[1], a[2]))
			conexao.encerra()
			return vetPessoa
		if(tipo == "leitor" or tipo == "jornalista"):
			conexao = Conexao()
			conexao.abre()
			conexao.cursor.execute("SELECT * FROM Pessoa WHERE tipo = %s", [tipo])
			vet = conexao.cursor.fetchall()
			vetPessoa = []
			for a in vet:
				vetPessoa.append(Pessoa(a[3], a[0], a[1], a[2]))
			conexao.encerra()
			return vetPessoa
		
	def editar(self, pessoa):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [pessoa.senha, pessoa.nome, pessoa.login]
		conexaoObj.cursor.execute("UPDATE Pessoa SET senha = MD5(%s), nome = %s WHERE login = %s;", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()		

	def excluir(self, login):
		conexaoObj = Conexao()
		conexaoObj.abre()
		conexaoObj.cursor.execute("DELETE FROM Pessoa WHERE login = %s;", [login])
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def obter(self, login):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Pessoa WHERE login = %s;", [login])
		a = conexao.cursor.fetchone()
		pessoa = Pessoa(a[3], a[0], a[1], a[2])
		conexao.encerra()
		return pessoa

class NoticiaDAO:

	def noticiaporAssunto(self, id):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Noticia WHERE idAssunto = %s;", [id])
		vet = conexao.cursor.fetchall()
		vetNoticia = []
		for a in vet:
			try:
				assunto = AssuntoDAO().obter(a[5])
			except TypeError:
				assunto = Assunto()
			vetNoticia.append(Noticia(a[1], a[2], a[3], a[4], assunto, a[0]))
		conexao.encerra()
		print (vetNoticia)
		return vetNoticia

	def procurar(self, busca):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Noticia WHERE titulo ILIKE %s;", ['%'+busca+'%'])
		vet = conexao.cursor.fetchall()
		vetNoticia = []
		for a in vet:
			try:
				assunto = AssuntoDAO().obter(a[5])
			except TypeError:
				assunto = Assunto()
			vetNoticia.append(Noticia(a[1], a[2], a[3], a[4], assunto, a[0]))
		conexao.encerra()
		print (vetNoticia)
		return vetNoticia	

	def adicionar(self, noticia):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [noticia.titulo, noticia.texto, noticia.data, noticia.foto, noticia.assunto.id]
		conexaoObj.cursor.execute("INSERT INTO Noticia (titulo, texto, data, foto,idAssunto) VALUES(%s, %s, %s, %s, %s) RETURNING id;", dados)
		conexaoObj.conexao.commit()
		id = conexaoObj.cursor.fetchone()[0]
		conexaoObj.encerra()
		return int(id)

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Noticia")
		vet = conexao.cursor.fetchall()
		vetNoticia = []
		for a in vet:
			try:
				assunto = AssuntoDAO().obter(a[5])
			except TypeError:
				assunto = Assunto()
			vetNoticia.append(Noticia(a[1], a[2], a[3], a[4], assunto, a[0]))
		conexao.encerra()
		return vetNoticia

	def editar(self, noticia):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [noticia.titulo, noticia.texto, noticia.data, noticia.foto, noticia.assunto.id, noticia.id]
		conexaoObj.cursor.execute("UPDATE Noticia SET titulo = %s, texto = %s, data = %s, foto = %s, idAssunto = %s WHERE id = %s;", dados)
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
		a = conexao.cursor.fetchone()
		try:
			assunto = AssuntoDAO().obter(a[5])
		except TypeError:
			assunto = Assunto()
		noticia = Noticia(a[1], a[2], a[3], a[4], assunto, a[0])
		conexao.encerra()
		return noticia

class ComentarioDAO:

	def adicionar(self, comentario):
		conexaoObj = Conexao()
		conexaoObj.abre()
		dados = [comentario.texto, comentario.data, comentario.noticia.id, comentario.pessoa.login]
		conexaoObj.cursor.execute("INSERT INTO Comentario (texto, data, idNoticia, loginPessoa) VALUES(%s, %s, %s, %s);", dados)
		conexaoObj.conexao.commit()
		conexaoObj.encerra()

	def listar(self):
		conexao = Conexao()
		conexao.abre()
		conexao.cursor.execute("SELECT * FROM Comentario")
		vet = conexao.cursor.fetchall()
		vetComentario = []
		for a in vet:
			try:
				noticia = NoticiaDAO().obter(a[3])
			except TypeError:
				noticia = Noticia()
			try:
				pessoa = PessoaDAO().obter(a[4])
			except TypeError:
				pessoa = Pessoa()
			vetComentario.append(Comentario(a[1], a[2], noticia, pessoa, a[0]))
		conexao.encerra()
		return vetComentario

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
			noticia = NoticiaDAO().obter(a[3])
		except TypeError:
			noticia = Noticia()
		try:
			pessoa = PessoaDAO().obter(a[4])
		except TypeError:
			pessoa = Pessoa()
		comentario = Comentario(a[1], a[2], noticia, pessoa, a[0])
		conexao.encerra()
		return comentario