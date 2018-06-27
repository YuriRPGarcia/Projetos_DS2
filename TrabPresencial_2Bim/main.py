from flask import * 
from persistencia import *
import os
from flask_uploads import*

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fotos/'
app.config['UPLOADS_DEFAULT_DEST'] = 'static/'
photos = UploadSet('fotos', IMAGES)
configure_uploads(app, photos)

@app.after_request
def depois_da_rota(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():	
    return render_template("index.html", vetAnotacoes = AnotacaoDAO().listar())

@app.route('/tela_cadastrar_anotacao')
def tela_cadastrar_pessoa():	
    return render_template("tela_cadastrar_anotacao.html")

@app.route('/tela_editar_anotacao/<id>')
def tela_editar_anotacao(id):	
    return render_template("tela_editar_anotacao.html", anotacao = AnotacaoDAO().obter(id))

@app.route('/cadastrar_anotacao', methods=['POST'])
def cadastrar_anotacao():
	anotacao = Anotacao()
	anotacao.titulo = str(request.form['titulo'])
	anotacao.texto = str(request.form['texto'])
	anotacaoDAO = AnotacaoDAO()
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			anotacao.id = anotacaoDAO.adicionar(anotacao)
			photos.save(f, folder=None, name=str(anotacao.id) + "." + extensao)
			anotacao.foto = str(anotacao.id) + "." + extensao
			anotacaoDAO.editar(anotacao)
		else:
			return render_template("tela_cadastrar_anotacao.html", mensagem = "formato de imagem nao suportado.")
	else:
		anotacaoDAO.adicionar(anotacao)
	return redirect(url_for("index"))

@app.route('/editar_anotacao', methods=['POST'])
def editar_anotacao():
	anotacao = AnotacaoDAO().obter(request.form['id'])
	anotacao.titulo = str(request.form['titulo'])
	anotacao.texto = str(request.form['texto'])
	anotacaoDAO = AnotacaoDAO()
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			os.remove(app.config['UPLOAD_FOLDER'] + anotacao.foto)
			photos.save(f, folder=None, name=str(anotacao.id) + "." + extensao)
			anotacao.foto = str(anotacao.id) + "." + extensao
		else:
			return render_template("tela_editar_anotacao.html", mensagem = "formato de imagem nao suportado.")
	anotacaoDAO.editar(anotacao)
	return redirect(url_for("index"))


@app.route('/excluir_anotacao/<id>')
def excluir_anotacao(id):
	anotacao = AnotacaoDAO().obter(id)
	if (anotacao.foto):
		try:
			os.remove(app.config['UPLOAD_FOLDER'] + anotacao.foto)
		except Exception as e:	
			anotacaoDAO = AnotacaoDAO()
			anotacaoDAO.excluir(id)			
	anotacaoDAO = AnotacaoDAO()
	anotacaoDAO.excluir(id)
	return redirect(url_for("index"))

if __name__=='__main__':
	app.run(debug=True)