#coding=UTF-8
import sys
from persistencia import *
from flask import *
# criando um objeto de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fotos/'
app.secret_key = "chave_secreta"

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.before_request
def antes_da_rota():
	if request.path != '/' and request.path != '/tela_login' and request.path != '/tela_cadastrar_aluno' and request.path != '/tela_cadastrar_empresa' and request.path != '/logar' and request.path != '/cadastrar_aluno' and request.path != '/cadastrar_empresa':
		if 'login' not in session and 'senha' not in session:		
			return redirect(url_for("index"))
		elif request.path == '/gerencia_alunos' or request.path == '/gerencia_empresas' or request.path == '/gerencia_estagios' or request.path == '/tela_admin_cadastra_estagio' or request.path == '/cadastra_estagio':
			if session['tipo'] != "admin":
				return redirect(url_for("redireciona_perfil"))
		elif request.path == '/tela_aluno_cadastra_estagio' or request.path == '/perfil_aluno':
			if session['tipo'] != "aluno":
				return redirect(url_for("redireciona_perfil"))
		elif request.path == '/tela_empresa_cadastra_estagio' or request.path == '/perfil_aluno':
			if session['tipo'] != "empresa":
				return redirect(url_for("redireciona_perfil"))

@app.route('/')
def index():	
    return render_template("index.html")

@app.route('/tela_login')
def tela_login():	
    return render_template("tela_login.html")

@app.route('/tela_admin_cadastra_estagio')
def tela_admin_cadastra_estagio():	
    return render_template("tela_admin_cadastra_estagio.html", vetAlunos = AlunoDAO().listar(), vetEmpresas = EmpresaDAO().listar())

@app.route('/gerencia_alunos')
def gerencia_alunos():	
    return render_template("gerencia_alunos.html", vetAlunos = AlunoDAO().listar())

@app.route('/gerencia_empresas')
def gerencia_empresas():	
    return render_template("gerencia_empresas.html", vetEmpresas = EmpresaDAO().listar())

@app.route('/gerencia_estagios')
def gerencia_estagios():	
    return render_template("gerencia_estagios.html", vetEstagios = EstagioDAO().listar())

@app.route('/logar', methods = ['POST'])
def logar():	
	
	login = request.form['login']
	senha = request.form['senha']
	try:
		aluno = AlunoDAO().obter(login)
	except TypeError:
		aluno = False
	try:
		empresa = EmpresaDAO().obter(login)
	except TypeError:
		empresa = False

	if (login == 'admin' and senha == 'admin'):
		session['login'] = login
		session['senha'] = senha
		session['tipo'] = "admin"
		return redirect(url_for("redireciona_perfil"))
	elif(empresa != False):
		if (login == empresa.cnpj and senha == empresa.senha):
			session['login'] = login
			session['senha'] = senha
			session['tipo'] = "empresa"
			return redirect(url_for("redireciona_perfil"))
	elif(aluno != False):
		if (login == aluno.matricula and senha == aluno.senha):
			session['login'] = login
			session['senha'] = senha
			session['tipo'] = "aluno"
			return redirect(url_for("redireciona_perfil"))
	elif(aluno == False and empresa == False):
		return render_template("tela_login.html", mensagem = "Login ou Senha Incorretos. Tente novamente")

@app.route('/redireciona_perfil')
def redireciona_perfil():	
		
	if 'login' not in session and 'senha' not in session:
		return redirect(url_for("tela_login"))
	else:
		login = session['login']
		senha = session['senha']
		try:
			aluno = AlunoDAO().obter(login)
		except TypeError:
			aluno = False
		try:
			empresa = EmpresaDAO().obter(login)
		except TypeError:
			empresa = False

		if (login == 'admin' and senha == 'admin'):
			return render_template("tela_admin.html")
		elif(empresa != False):
			if (login == empresa.cnpj and senha == empresa.senha):
				return redirect(url_for("perfil_empresa"))
		elif(aluno != False):
			if (login == aluno.matricula and senha == aluno.senha):
				return redirect(url_for("perfil_aluno"))

@app.route("/logout")
def logout():
	session.pop('login', None)
	session.pop('senha', None)
	return redirect(url_for("index"))

# ALUNOS

@app.route('/perfil_aluno')
def perfil_aluno():	
    return render_template("perfil_aluno.html", aluno = AlunoDAO().obter(session['login']), vetEstagios = EstagioDAO().listar_porAluno(session['login']))

@app.route('/tela_cadastrar_aluno')
def tela_cadastrar_aluno():	
    return render_template("tela_cadastrar_aluno.html")

@app.route('/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():	
	try:
		alunoaux = AlunoDAO().obter(str(request.form['matricula']))
	except TypeError:
		alunoaux = False

	if alunoaux == False:
		aluno = Aluno()
		aluno.matricula = str(request.form['matricula'])
		aluno.nome = str(request.form['nome'])
		aluno.senha = str(request.form['senha'])
		alunoDAO = AlunoDAO()

		# se ha arquivo vindo do form
		if ('foto' in request.files):

			f = request.files['foto']	
			
			extensao = f.filename.rsplit('.', 1)[1].lower()

			if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):

				f.save(app.config['UPLOAD_FOLDER'] + str(request.form['matricula']) + "." + extensao)

				aluno.foto = str(request.form['matricula']) + "." + extensao
			
			else:
				return render_template("tela_cadastrar_aluno.html", mensagem = "formato de imagem nao suportado.")

		alunoDAO.adicionar(aluno)

		if (session['tipo'] == "admin"):
			return redirect(url_for('gerencia_alunos'))

		return redirect(url_for("index"))

	elif alunoaux != False:
		return render_template("tela_cadastrar_aluno.html", mensagem = "Matrícula já existente.") 

@app.route('/tela_alterar_aluno/<matricula>')
def tela_alterar_aluno(matricula):	
    if matricula == session['login'] or session['login'] == "admin":
    	return render_template("tela_alterar_aluno.html", aluno = AlunoDAO().obter(matricula))
    else:
    	return redirect(url_for("index"))

@app.route('/altera_aluno', methods=['POST'])
def altera_aluno():	
	aluno = Aluno()
	aluno.matricula = str(request.form['matricula'])
	aluno.nome = str(request.form['nome'])
	aluno.senha = str(request.form['senha'])
	alunoDAO = AlunoDAO()
	
	# se ha arquivo vindo do form
	if ('foto' in request.files):

		f = request.files['foto']	
		
		extensao = f.filename.rsplit('.', 1)[1].lower()

		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):

			f.save(app.config['UPLOAD_FOLDER'] + str(session['login']) + "." + extensao)

			aluno.foto = str(session['login']) + "." + extensao

		else:
			return render_template("tela_alterar_aluno.html", mensagem = "formato de imagem nao suportado.")

	alunoDAO.editar(aluno)

	if (session['tipo'] == "admin"):
		return redirect(url_for('gerencia_alunos'))
	else:
		return redirect(url_for("redireciona_perfil"))

@app.route('/tela_aluno_cadastra_estagio')
def tela_aluno_cadastra_estagio():	
    return render_template("tela_aluno_cadastra_estagio.html", vetEmpresas = EmpresaDAO().listar())

@app.route("/excluir_aluno/<matricula>")
def excluir_aluno(matricula):
	alunoDAO = AlunoDAO()
	if matricula == session['login'] or session['login'] == "admin":
		alunoDAO.excluir(matricula)
		if (session['tipo'] == "admin"):
			return redirect(url_for('gerencia_alunos'))
		return redirect(url_for('logout'))
	else:
		return redirect(url_for('index'))

# EMPRESAS

@app.route('/perfil_empresa')
def perfil_empresa():	
    return render_template("perfil_empresa.html", empresa = EmpresaDAO().obter(session['login']), vetEstagios = EstagioDAO().listar_porEmpresa(session['login']))

@app.route('/tela_cadastrar_empresa')
def tela_cadastrar_empresa():	
    return render_template("tela_cadastrar_empresa.html")

@app.route('/cadastrar_empresa', methods=['POST'])
def cadastrar_empresa():	
	try:
		empresaux = EmpresaDAO().obter(str(request.form['cnpj']))
	except TypeError:
		empresaux = False	

	if empresaux == False:
		empresa = Empresa()
		empresa.cnpj = str(request.form['cnpj'])
		empresa.nome = str(request.form['nome'])
		empresa.senha = str(request.form['senha'])
		empresaDAO = EmpresaDAO()
		
		# se ha arquivo vindo do form
		if ('logo' in request.files):

			f = request.files['logo']
			
			extensao = f.filename.rsplit('.', 1)[1].lower()

			if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):

				f.save(app.config['UPLOAD_FOLDER'] + str(request.form['cnpj']) + "." + extensao)

				empresa.logo = str(request.form['cnpj']) + "." + extensao
			
			else:
				return render_template("tela_cadastrar_empresa.html", mensagem = "formato de imagem nao suportado.")

		empresaDAO.adicionar(empresa)

		if (session['tipo'] == "admin"):
			return redirect(url_for('gerencia_empresas'))

		return redirect(url_for("index"))	

	elif empresaux != False:
		return render_template("tela_cadastrar_empresa.html", mensagem = "CNPJ já cadastrado.")


@app.route('/tela_empresa_cadastra_estagio')
def tela_empresa_cadastra_estagio():	
    return render_template("tela_empresa_cadastra_estagio.html", vetAlunos = AlunoDAO().listar())

@app.route('/tela_alterar_empresa/<cnpj>')
def tela_alterar_empresa(cnpj):	
    if cnpj == session['login'] or session['login'] == "admin":
    	return render_template("tela_alterar_empresa.html", empresa = EmpresaDAO().obter(cnpj))
    else:
    	return redirect(url_for("index"))

@app.route('/altera_empresa', methods=['POST'])
def altera_empresa():	
	empresa = Empresa()
	empresa.cnpj = str(request.form['cnpj'])
	empresa.nome = str(request.form['nome'])
	empresa.senha = str(request.form['senha'])
	empresaDAO = EmpresaDAO()

	# se ha arquivo vindo do form
	if ('logo' in request.files):
		f = request.files['logo']		
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			f.save(app.config['UPLOAD_FOLDER'] + str(session['login']) + "." + extensao)
			empresa.logo = str(session['login']) + "." + extensao		
			empresaDAO.editar(empresa)
		else:
			return render_template("tela_alterar_empresa.html", empresa = empresa, mensagem = "formato de imagem nao suportado.")
	else:
		empresaDAO.editar(empresa)	# return "oi"


	if (session['tipo'] == "admin"):
		return redirect(url_for('gerencia_empresas'))
	else:
		return redirect(url_for("redireciona_perfil"))

@app.route('/excluir_empresa/<cnpj>')
def excluir_empresa(cnpj):	
	empresaDAO = EmpresaDAO()
	if cnpj == session['login'] or session['login'] == "admin":
		empresaDAO.excluir(cnpj)
		if (session['tipo'] == "admin"):
			return redirect(url_for('gerencia_empresas'))
		return redirect(url_for('logout'))
	else:
		return redirect(url_for("index"))

# ESTAGIO

@app.route('/cadastra_estagio', methods=['POST'])
def cadastra_estagio():	
	  estagio = Estagio()
	  estagio.empresa = EmpresaDAO().obter(request.form['empresa'])
	  estagio.aluno = AlunoDAO().obter(request.form['aluno'])
	  estagio.dataInicio = request.form['dataInicio']
	  estagio.dataFim = request.form['dataFim']
	  estagioDAO = EstagioDAO()
	  estagioDAO.adicionar(estagio)
	  return redirect(url_for("gerencia_estagios"))

@app.route('/aluno_cadastra_estagio', methods=['POST'])
def aluno_cadastra_estagio():	
	  estagio = Estagio()
	  estagio.empresa = EmpresaDAO().obter(request.form['empresa'])
	  estagio.aluno = AlunoDAO().obter(session['login'])
	  estagio.dataInicio = request.form['dataInicio']
	  estagio.dataFim = request.form['dataFim']
	  estagioDAO = EstagioDAO()
	  estagioDAO.adicionar(estagio)
	  return redirect(url_for("redireciona_perfil"))

@app.route('/empresa_cadastra_estagio', methods=['POST'])
def empresa_cadastra_estagio():	
	  estagio = Estagio()
	  estagio.empresa = EmpresaDAO().obter(session['login'])
	  estagio.aluno = AlunoDAO().obter(request.form['aluno'])
	  estagio.dataInicio = request.form['dataInicio']
	  estagio.dataFim = request.form['dataFim']
	  estagioDAO = EstagioDAO()
	  estagioDAO.adicionar(estagio)
	  return redirect(url_for("redireciona_perfil"))

@app.route('/tela_altera_estagio/<cod>')
def tela_altera_estagio(cod):
	estagio = EstagioDAO().obter(cod)
	if estagio.aluno.matricula == session['login'] or estagio.empresa.cnpj == session['login'] or session['login'] == "admin":
		return render_template("tela_altera_estagio.html", estagio = EstagioDAO().obter(cod))
	else:
		return redirect(url_for("index"))
    	
@app.route('/altera_estagio', methods=['POST'])
def altera_estagio():	
	estagio = Estagio()
	estagio.cod = request.form['cod']
	estagio.dataInicio = request.form['dataInicio']
	estagio.dataFim = request.form['dataFim']
	estagioDAO = EstagioDAO()
	estagioDAO.editar(estagio)
	if (session['tipo'] == "admin"):
		return redirect(url_for('gerencia_estagios'))
	else:
		return redirect(url_for("redireciona_perfil"))

@app.route('/excluir_estagio/<cod>')
def excluir_estagio(cod):	
	estagioDAO = EstagioDAO()
	estagio = estagioDAO.obter(cod)
	if estagio.aluno.matricula == session['login'] or estagio.empresa.cnpj == session['login'] or session['login'] == "admin":
		estagioDAO.excluir(cod)
		if (session['tipo'] == "admin"):
			return redirect(url_for("gerencia_estagios"))
		return redirect(url_for("redireciona_perfil"))
	else:
		return redirect(url_for("index"))

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('UTF-8')
	app.run(debug=True)
			