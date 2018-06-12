class Assunto:
	def __init__(self, nome = "", id = 0): 
		self.nome = nome
		self.id = id

	def __repr__(self):
		return self.id + ";" + self.nome

class Noticia:
	def __init__(self, titulo = "", texto = "", data = "", assunto = Assunto(), id = 0):
		self.titulo = titulo
		self.texto = texto
		self.data = data
		self.assunto = assunto
		self.id = id

	def __repr__(self):
		return self.id + ";" + self.titulo + ";" + self.texto + ";" + self.data + ";" + self.assunto

class Comentario:
	def __init__(self, texto = "", data = "", noticia = Noticia(), leitor = Leitor(), id = 0)
		self.texto = texto
		self.data = data
		self.noticia = noticia
		self.leitor = leitor
		self.id = id

	def __repr__(self)
		return self.id + ";" + self.texto + ";" + self.data + ";" + self.noticia + ";" + self.leitor