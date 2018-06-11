class Aluno:
	def __init__(self, matricula = "", nome = "", senha = "", foto = ""):
		self.matricula = matricula
		self.nome = nome
		self.senha = senha
		self.foto = foto

	def __repr__(self):
		return self.matricula + ";" + self.nome + ";" +	self.senha + ";" + self.foto

class Empresa:
	def __init__(self, cnpj = "", nome = "", logo = "", senha = ""):
		self.cnpj = cnpj
		self.nome = nome
		self.logo = logo
		self.senha = senha

	def __repr__(self):
		return self.cnpj + ";" + self.nome + ";" + self.logo + ";" + self.senha

class Estagio:
	def __init__(self, cod = 0, empresa = Empresa(), aluno = Aluno(), dataInicio = "", dataFim = ""):
		self.cod = cod
		self.empresa = empresa
		self.aluno = aluno
		self.dataInicio = dataInicio
		self.dataFim = dataFim

	def __repr__(self):
		return self.cod + ";" + self.empresa + ";" + self.aluno + ";" + self.dataInicio + ";" + self.dataFim	
		
	
		