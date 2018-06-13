from flask import * 
from persistencia import *
import os
from jinja2 import TemplateNotFound
import datetime

administracao = Blueprint('administracao', __name__,
                        template_folder='administracao/templates', static_folder = 'administracao/static')

@administracao.before_request
def antes():	
	app.logger.debug(request.path)
	if ("/administracao/" in request.path):			
		if (('login' not in session and 'senha' not in session) or session['tipo'] != 'admin' or session['tipo'] != 'jornalista'):
			app.logger.warning("entrou no segundo...")
			return "erro...faca login corretamente"

@administracao.route('/')
def gerencia():	
    return render_template("gerencia.html")

@administracao.route('/tela_cadastrar_noticia')
def tela_cadastrar_noticia():
	return render_template("tela_cadastrar_noticia.html")

@administracao.route('/cadastrar_noticia', methods=['POST'])
def cadastrar_noticia():
	noticia = Noticia()
	noticia.titulo = str(request.form('titulo'))
	noticia.texto = str(request.form('texto'))
	noticia.data = datetime.date.today()
	noticia.assunto = AssuntoDAO().obter(request.form('assunto'))
	noticiaDAO = NoticiaDAO()
	noticiaDAO.adicionar(noticia)
	if ('foto' in request.files):
		noticiaDAO.obter(noticia.id)
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			f.save(app.config['UPLOAD_FOLDER'] + str(noticia.id) + "." + extensao)
			noticia.foto = str(noticia.id) + "." + extensao
			noticiaDAO.editar(noticia)
		else:
			return render_template("tela_cadastrar_noticia.html", mensagem = "formato de imagem nao suportado.")
	return redirect(url_for("/administracao/"))

@administracao.route('/tela_editar_noticia/<id>')
def tela_editar_noticia(id):
	return render_template("tela_editar_noticia.html", noticia = NoticiaDAO.obter(id))

@administracao.route('/editar_noticia', methods=['POST'])
def editar_noticia():
	noticia = NoticiaDAO().obter(request.form('id'))
	noticia.titulo = str(request.form('titulo'))
	noticia.texto = str(request.form('texto'))
	noticia.data = datetime.date.today()
	noticia.assunto = AssuntoDAO().obter(request.form('assunto'))
	noticiaDAO = NoticiaDAO()
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			f.save(app.config['UPLOAD_FOLDER'] + str(noticia.id) + "." + extensao)
			noticia.foto = str(noticia.id) + "." + extensao
		else:
			return render_template("tela_cadastrar_noticia.html", mensagem = "formato de imagem nao suportado.")
	noticiaDAO.editar(noticia)
	return redirect(url_for("/administracao/"))

@app.route('/excluir_noticia/<id>')
def excluir_noticia(id):
	if session['tipo'] == "jornalista" or session['tipo'] == "admin":
		assunto = AssuntoDAO().obter(id)
		if (jogador.foto):
			try:
				os.remove(app.config['UPLOAD_FOLDER'] + assunto.foto)				
			except Exception as e:			
				return render_template("gerencia.html", mensagem = "imagem nao encontrada. nao foi possivel excluir o jogador...")			
		assuntoDAO = AssuntoDAO()
		assuntoDAO.excluir(id)
	return redirect(url_for("/administracao/"))

@administracao.route('/cadastrar_assunto', methods=['POST'])
def cadastrar_assunto():
	assunto = Assunto(request.form('nome'))
	assuntoDAO = AssuntoDAO()
	assuntoDAO.adicionar(assunto) 
	return redirect(url_for("/administracao/"))

@administracao.route('/editar_assunto', methods=['POST'])
def editar_assunto():
	assunto = Assunto(request.form('nome'))
	assuntoDAO = AssuntoDAO()
	assuntoDAO.editar(assunto) 
	return redirect(url_for("/administracao/"))

@app.route('/excluir_assunto/<id>')
def excluir_pessoa(id):
	if session['tipo'] == "jornalista" or session['tipo'] == "admin":
		assuntoDAO = AssuntoDAO()
		assuntoDAO.excluir(id)
	return redirect(url_for("/administracao/"))



app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(administracao, url_prefix='/administracao')

@app.after_request
def depois_da_rota(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():	
    return render_template("index.html")

@app.route('/tela_cadastrar_pessoa')
def tela_cadastrar_pessoa():	
    return render_template("tela_cadastrar_pessoa.html")

@app.route('/cadastrar_pessoa', methods=['POST'])
def cadastrar_pessoa():
	try:
		pessoaux = PessoaDAO().obter(str(request.form['login']))
	except TypeError:
		pessoaux = False
	if pessoaux == False:
		pessoa = Pessoa()
		pessoa.login = str(request.form['login'])
		pessoa.senha = str(request.form['senha'])
		pessoa.nome = str(request.form['nome'])
		if session['tipo'] == 'admin':
			pessoa.tipo == "jornalista"
		else:
			pessoa.tipo = "leitor"
		pessoaDAO = PessoaDAO()
		pessoaDAO.adicionar(pessoa)
	else:
		return render_template("tela_cadastrar_pessoa.html", mensagem = "Login já existente.")

@app.route('/tela_editar_pessoa/<login>')
def tela_editar_pessoa(login):	
    if login == session['login'] or session['tipo'] == "admin":
    	return render_template("tela_alterar_aluno.html", pessoa = PessoaDAO().obter(login))

@app.route('/editar_pessoa', methods=['POST'])
def editar_pessoa():
	pessoa = PessoaDAO().obter(str(request.form['login']))
	pessoa.senha = str(request.form['senha'])
	pessoa.nome = str(request.form['nome'])
	pessoaDAO = PessoaDAO()
	pessoaDAO.editar(pessoa)
	return render_template("tela_cadastrar_pessoa.html", mensagem = "Login já existente.")

@app.route('/excluir_pessoa/<login>')
def excluir_pessoa(login):
	if login == session['login'] or session['tipo'] == "admin":
		pessoaDAO = PessoaDAO()
		pessoaDAO.excluir(login)
		return redirect(url_for("/"))

@app.route('/comentar', methods=['POST'])
def comentar():
	if (session['login'] is not None) and (session['login'] is not None) and session['tipo'] == "leitor":
		comentario = Comentario()
		comentario.noticia = NoticiaDAO().obter(request.form['noticia'])
		comentario.pessoa = PessoaDAO().obter(session['login']) 
		comentario.texto = str(request.form['texto'])
		comentario.data = datetime.date.today()
		comentarioDAO = ComentarioDAO()
		comentarioDAO.adicionar(comentario)

@app.route('/editar_comentario/<id>', methods=['POST'])
def editar_comentario(id):
	if session['login'] == NoticiaDAO().obter(request.form['noticia']) or session['tipo'] == "admin" or session['tipo'] == "jornalista":
		comentario = ComentarioDAO().obter(id) 
		comentario.texto = str(request.form['texto'])
		comentario.data = datetime.date.today()
		comentarioDAO = ComentarioDAO()
		comentarioDAO.editar(comentario)

@app.route('/excluir_comentario/<id>')
def excluir_comentario(id):
	if session['login'] == NoticiaDAO().obter(request.form['noticia']) or session['tipo'] == "admin" or session['tipo'] == "jornalista":
		comentarioDAO = ComentarioDAO()
		comentarioDAO.excluir(id) 

@app.route('/tela_login')
def tela_login():	
    return render_template("tela_login.html")

@app.route('/logar', methods = ['POST'])
def logar():	
	login = request.form['login']
	senha = request.form['senha']
	try:
		pessoa = AlunoDAO().obter(login)
	except TypeError:
		pessoa = False

	if (login == 'bae60998ffe4923b131e3d6e4c19993e' and senha == '8d70e0d1acb06b4648c7aa8927509660'):
		session['login'] = login
		session['senha'] = senha
		session['tipo'] = "admin"
		return redirect(url_for("/admin/"))
	elif(pessoa != False):
		if (login == empresa.cnpj and senha == empresa.senha):
			session['login'] = login
			session['senha'] = senha
			session['tipo'] = pessoa.tipo
			if pessoa.tipo == "jornalista":
				return redirect(url_for("/"))
			if pessoa.tipo == "leitor":
				return redirect(url_for("/"))
	else:
		return render_template("tela_login.html", mensagem = "Login ou Senha Incorretos. Tente novamente")

@app.route("/logout")
def logout():
	session.pop('login', None)
	session.pop('senha', None)
	session.pop('tipo', None)
	return redirect(url_for("index"))


if __name__=='__main__':
	app.run(debug=True)