class Assunto:
	def __init__(self, nome = "", id = 0): 
		self.nome = nome
		self.id = id

	def __repr__(self):
		return str(self.id) + ";" + self.nome

class Noticia:
	def __init__(self, titulo = "", texto = "", data = "", foto = "", assunto = Assunto(), id = 0):
		self.titulo = titulo
		self.texto = texto
		self.data = data
		self.assunto = assunto
		self.id = id
		self.foto = foto

	def __repr__(self):
		return str(self.id) + ";" + self.titulo + ";" + self.texto + ";" + str(self.data) + ";" + self.foto + ";" + str(self.assunto)

class Pessoa:
	def __init__(self, tipo = "", login = "", senha = "", nome = ""):
		self.tipo = tipo
		self.login = login
		self.senha = senha
		self.nome = nome

	def __repr__(self):
		return self.tipo + ";" + self.login + ";" + self.senha + ";" + self.nome

class Comentario:
	def __init__(self, texto = "", data = "", noticia = Noticia(), pessoa = Pessoa("leitor"), id = 0):
		self.texto = texto
		self.data = data
		self.noticia = noticia
		self.pessoa = pessoa
		self.id = id

	def __repr__(self):
		return self.id + ";" + self.texto + ";" + self.data + ";" + self.noticia + ";" + self.pessoa

