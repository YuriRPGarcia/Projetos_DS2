from flask import * 
import hashlib
from persistencia import *
import os
from jinja2 import TemplateNotFound
import datetime
import json
from flask_mail import *
from flask_uploads import *

administracao = Blueprint('administracao', __name__,
                        template_folder='administracao/templates', static_folder = 'static')

@administracao.before_request
def antes():	
	app.logger.debug(request.path)
	if ("/administracao/" in request.path):			
		if (('login' not in session and 'senha' not in session) or session['tipo'] != 'admin' and session['tipo'] != 'jornalista'):
			app.logger.warning("entrou no segundo...")
			return redirect(url_for("admLogin"))

@administracao.route('/')
def gerencia():	
    return render_template("gerencia.html", vetAssunto = AssuntoDAO().listar())

@administracao.route('/jornalistas')
def jornalistas():	
    return render_template("jornalistas.html", vetPessoas = PessoaDAO().listar("jornalista"))

@administracao.route('/tela_cadastrar_noticia')
def tela_cadastrar_noticia():
	return render_template("tela_cadastrar_noticia.html", vetAssunto = AssuntoDAO().listar())

@administracao.route('/cadastrar_noticia', methods=['POST'])
def cadastrar_noticia():
	noticia = Noticia()
	noticia.titulo = str(request.form['titulo'])
	noticia.texto = str(request.form['texto'])
	noticia.data = datetime.date.today()
	noticia.assunto = AssuntoDAO().obter(request.form['assunto'])
	noticiaDAO = NoticiaDAO()
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			noticia.id = noticiaDAO.adicionar(noticia)
			photos.save(f, folder=None, name=str(noticia.id) + "." + extensao)
			noticia.foto = str(noticia.id) + "." + extensao
			noticiaDAO.editar(noticia)
			emails = EmailDAO().listar()
			with mail.connect() as conn:
				for n in emails:
					msg = Message(recipients=[n], body = noticia.titulo, subject="Uma nova notícia foi publicada")
					conn.send(msg)
		else:
			return render_template("tela_cadastrar_noticia.html", mensagem = "formato de imagem nao suportado.")
	else:
		noticiaDAO.adicionar(noticia)
	return redirect(url_for("administracao.gerencia"))

@administracao.route('/tela_editar_noticia/<id>')
def tela_editar_noticia(id):
	return render_template("tela_editar_noticia.html", noticia = NoticiaDAO().obter(id), vetAssunto = AssuntoDAO().listar())

@administracao.route('/editar_noticia', methods=['POST'])
def editar_noticia():
	noticia = NoticiaDAO().obter(request.form['id'])
	noticia.titulo = str(request.form['titulo'])
	noticia.texto = str(request.form['texto'])
	noticia.data = datetime.date.today()
	noticia.assunto = AssuntoDAO().obter(request.form['assunto'])
	noticiaDAO = NoticiaDAO()
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			os.remove(app.config['UPLOAD_FOLDER'] + noticia.foto)
			photos.save(f, folder=None, name=str(noticia.id) + "." + extensao)
			noticia.foto = str(noticia.id) + "." + extensao
		else:
			return render_template("tela_editar_noticia.html", mensagem = "formato de imagem nao suportado.")
	noticiaDAO.editar(noticia)
	return redirect(url_for("noticia", id = request.form['id']))

@administracao.route('/excluir_noticia/<id>')
def excluir_noticia(id):
	if session['tipo'] == "jornalista" or session['tipo'] == "admin":
		noticia = NoticiaDAO().obter(id)
		if (noticia.foto):
			try:
				os.remove(app.config['UPLOAD_FOLDER'] + noticia.foto)				
			except Exception as e:			
				return render_template("gerencia.html", mensagem = "imagem nao encontrada. nao foi possivel excluir o jogador...")			
		noticiaDAO = NoticiaDAO()
		noticiaDAO.excluir(id)
	return redirect(url_for("administracao.gerencia"))

@administracao.route('/cadastrar_assunto', methods=['POST'])
def cadastrar_assunto():
	assunto = Assunto()
	assunto.nome = str(request.form['nome'])
	assuntoDAO = AssuntoDAO()
	assuntoDAO.adicionar(assunto)
	assunto = assuntoDAO.obterporNome(request.form['nome'])
	return jsonify(id=assunto.id, nome=assunto.nome)
	

@administracao.route('/editar_assunto', methods=['POST'])
def editar_assunto():
	assunto = Assunto(request.form['nome'])
	assuntoDAO = AssuntoDAO()
	assuntoDAO.editar(assunto) 
	return redirect(url_for("administracao.gerencia"))

@administracao.route('/excluir_assunto/<id>')
def excluir_pessoa(id):
	if session['tipo'] == "jornalista" or session['tipo'] == "admin":
		assuntoDAO = AssuntoDAO()
		assuntoDAO.excluir(id)
		return redirect(url_for("administracao.gerencia"))
	else:
		return redirect(url_for("administracao.gerencia"))



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fotos/'
app.config['UPLOADS_DEFAULT_DEST'] = 'static/'
photos = UploadSet('fotos', IMAGES)
configure_uploads(app, photos)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.register_blueprint(administracao, url_prefix='/administracao')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ("JN>Omelete", "yurirodsk8@gmail.com")
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.after_request
def depois_da_rota(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/admLogin')
def admLogin():
	return render_template("admLogin.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():	
    return render_template("index.html", vetAssunto = AssuntoDAO().listar())

@app.route('/email', methods=['POST'])
def email():	
    email = str(request.form['email'])
    emailDAO = EmailDAO().adicionar(email)
    return jsonify(mensagem = "E-mail cadastrado, você receberá as notícias.")

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
		if 'tipo' not in session or session['tipo'] == "leitor":
			pessoa.tipo = "leitor"
		elif session['tipo'] == "admin":
			pessoa.tipo = "jornalista"		
			pessoaDAO = PessoaDAO()
			pessoaDAO.adicionar(pessoa)
			return redirect(url_for("administracao.gerencia"))
		pessoaDAO = PessoaDAO()
		pessoaDAO.adicionar(pessoa)
		return redirect(url_for("index"))
	else:
		return render_template("tela_cadastrar_pessoa.html", mensagem = "Login já existente.")

@app.route('/tela_editar_pessoa/<login>')
def tela_editar_pessoa(login):	
    if login == session['login'] or session['tipo'] == "admin":
    	return render_template("tela_editar_pessoa.html", pessoa = PessoaDAO().obter(login))

@app.route('/editar_pessoa', methods=['POST'])
def editar_pessoa():
	pessoa = PessoaDAO().obter(str(request.form['login']))
	pessoa.senha = str(request.form['senha'])
	pessoa.nome = str(request.form['nome'])
	pessoaDAO = PessoaDAO()
	pessoaDAO.editar(pessoa)
	if session['login'] == "admin" :
		return redirect(url_for("jornalistas"))
	elif session['login'] == "jornalista":
		return redirect(url_for("administracao.gerencia"))
	else:
		return redirect(url_for("index"))

@app.route('/excluir_pessoa/<login>')
def excluir_pessoa(login):
	if login == session['login'] or session['tipo'] == "admin":
		pessoaDAO = PessoaDAO()
		pessoaDAO.excluir(login)
	if session['login'] == "admin" :
		return redirect(url_for("jornalistas"))
	else:
		return redirect(url_for("index"))
		return redirect(url_for("logout"))

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
		return redirect(url_for("noticia", id = request.form['noticia']))

@app.route('/editar_comentario/<id>', methods=['POST'])
def editar_comentario(id):
	comentario = ComentarioDAO().obter(id)
	if session['login'] == comentario.pessoa.login or session['tipo'] == "admin" or session['tipo'] == "jornalista":
		comentario.texto = str(request.form['texto'])
		comentario.data = datetime.date.today()
		comentarioDAO = ComentarioDAO()
		comentarioDAO.editar(comentario)
		return redirect(url_for("noticia", id = comentario.noticia.id))

@app.route('/excluir_comentario/<id>')
def excluir_comentario(id):
	comentario = ComentarioDAO().obter(id)
	if session['login'] == comentario.pessoa.login or session['tipo'] == "admin" or session['tipo'] == "jornalista":
		comentarioDAO = ComentarioDAO()
		comentarioDAO.excluir(id)
		return redirect(url_for("noticia", id = comentario.noticia.id))		 

@app.route('/tela_login')
def tela_login():	
    return render_template("tela_login.html")

@app.route('/logar', methods = ['POST'])
def logar():	
	login = request.form['login']
	senha = request.form['senha']
	try:
		pessoa = PessoaDAO().obter(login)
	except TypeError:
		pessoa = False

	if (login == 'bae60998ffe4923b131e3d6e4c19993e' and senha == 'bae60998ffe4923b131e3d6e4c19993e'):
		session['login'] = login
		session['senha'] = senha
		session['tipo'] = "admin"
		return redirect("/administracao/")
	elif(pessoa != False):
		senha = hashlib.md5(bytes(senha,"ascii"))
		senha = str(senha.hexdigest())
		if (login == pessoa.login and senha == pessoa.senha):
			session['login'] = login
			session['senha'] = senha
			session['tipo'] = pessoa.tipo
			if pessoa.tipo == "jornalista":
				return redirect(url_for("index"))
			elif pessoa.tipo == "leitor":
				return redirect(url_for("index"))
		return render_template("tela_login.html", mensagem = "Login ou Senha Incorretos. Tente novamente")
	else:
		return render_template("tela_login.html", mensagem = "Login ou Senha Incorretos. Tente novamente")

@app.route("/logout")
def logout():
	session.pop('login', None)
	session.pop('senha', None)
	session.pop('tipo', None)
	return redirect(url_for("index"))

@app.route('/procurar_noticias', methods = ['POST'])
def procurar_noticias():
	busca = str(request.form['busca'])
	return render_template("noticias.html", vetNoticia = NoticiaDAO().procurar(busca))

@app.route('/busca_autoComplete', methods = ['POST'])
def busca_autoComplete():
	busca = str(request.form['busca'])
	vetAuxNoticia = NoticiaDAO().procurar(busca)
	vetNoticia = []
	if len(busca) > 0:
		for n in vetAuxNoticia:
			vetNoticia.append(n.obj2Str())
		return jsonify(vetNoticia = vetNoticia)

@app.route('/noticia/<id>')
def noticia(id):
	return render_template("noticia.html", noticia = NoticiaDAO().obter(id), vetComentario = ComentarioDAO().listar())

@app.route('/noticia_assunto/<id>')
def noticia_assunto(id):
	return render_template("noticia_assunto.html", vetNoticia = NoticiaDAO().noticiaporAssunto(id))



if __name__=='__main__':
	app.run(debug=True)