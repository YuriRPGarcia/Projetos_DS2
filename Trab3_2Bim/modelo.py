class Filme:
	
	def __init__(self, cod = 0, titulo = "", sinopse = "", genero = "", foto = "", dataInicio = "", dataFim = ""):
		self.cod = cod
		self.titulo = titulo
		self.sinopse = sinopse
		self.genero = genero
		self.dataInicio = dataInicio
		self.dataFim = dataFim
		self.foto = foto

	def __repr__(self):
		return self.cod + self.titulo + self.sinopse + self.genero + self.dataInicio + self.dataFim + self.foto

class Sessao:
	
	def __init__(self, cod = 0, dia = "", hora = "", codFilme = 0):
		self.dia = dia
		self.hora = hora
		self.codFilme = codFilme
		self.cod = cod

	def __repr__(self):
		return self.cod + self.dia + self.hora + self.codFilme

class Ingresso:

	def __init__(self, cod = 0, nomeCliente = "", cadeira = 0, codSessao = 0):
		self.nomeCliente = nomeCliente
		self.cadeira = cadeira
		self.codSessao = codSessao
		self.cod = cod

	def __repr__(self):
		return self.cod + self.nomeCliente + self.cadeira + self.codSessao

		