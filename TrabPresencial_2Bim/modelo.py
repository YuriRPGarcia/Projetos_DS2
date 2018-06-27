class Anotacao:
	def __init__(self, titulo = "", texto = "", foto = "", id = 0):
		self.titulo = titulo
		self.texto = texto
		self.id = id
		self.foto = foto

	def obj2Str(self):
		return str(self.id) + ";" + str(self.titulo)
