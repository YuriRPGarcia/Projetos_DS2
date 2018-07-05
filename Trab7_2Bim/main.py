from flask import * 
import os
from flask_uploads import*
from flask_sqlalchemy import*

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fotos/'
app.config['UPLOADS_DEFAULT_DEST'] = 'static/'
photos = UploadSet('fotos', IMAGES)
configure_uploads(app, photos)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/Anotacoes'
db = SQLAlchemy(app)

class Anotacao(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(100), unique=False, nullable=True)
	texto = db.Column(db.String(500), unique=False, nullable=True)
	foto = db.Column(db.String(500), unique=False, nullable=True)

@app.after_request
def depois_da_rota(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():	
    return render_template("index.html", vetAnotacoes = Anotacao.query.all())

@app.route('/tela_cadastrar_anotacao')
def tela_cadastrar_pessoa():	
    return render_template("tela_cadastrar_anotacao.html")

@app.route('/tela_editar_anotacao/<id>')
def tela_editar_anotacao(id):	
    return render_template("tela_editar_anotacao.html", anotacao = Anotacao.query.filter_by(id = id).first())

@app.route('/cadastrar_anotacao', methods=['POST'])
def cadastrar_anotacao():
	anotacao = Anotacao()
	anotacao.titulo = str(request.form['titulo'])
	anotacao.texto = str(request.form['texto'])
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			db.session.add(anotacao)
			db.session.flush()
			photos.save(f, folder=None, name=str(anotacao.id) + "." + extensao)
			anotacao.foto = str(anotacao.id) + "." + extensao
			db.session.commit()
		else:
			return render_template("tela_cadastrar_anotacao.html", mensagem = "formato de imagem nao suportado.")
	else:
		db.session.commit()
	return redirect(url_for("index"))

@app.route('/editar_anotacao', methods=['POST'])
def editar_anotacao():
	anotacao = Anotacao.query.filter_by(id = request.form['id']).first()
	anotacao.titulo = str(request.form['titulo'])
	anotacao.texto = str(request.form['texto'])
	if ('foto' in request.files):
		f = request.files['foto']	
		extensao = f.filename.rsplit('.', 1)[1].lower()
		if (extensao == 'png' or extensao == 'jpg' or extensao == 'jpeg'):
			os.remove(app.config['UPLOAD_FOLDER'] + anotacao.foto)
			photos.save(f, folder=None, name=str(anotacao.id) + "." + extensao)
			anotacao.foto = str(anotacao.id) + "." + extensao
			db.session.commit()
		else:
			return render_template("tela_editar_anotacao.html", mensagem = "formato de imagem nao suportado.")
	else:
		db.session.commit()
	return redirect(url_for("index"))

@app.route('/excluir_anotacao/<id>')
def excluir_anotacao(id):
	anotacao = Anotacao.query.filter_by(id = id).first()
	if (anotacao.foto):
		try:
			os.remove(app.config['UPLOAD_FOLDER'] + anotacao.foto)
		except Exception as e:	
			pass		
	db.session.delete(anotacao)
	db.session.commit()
	return redirect(url_for("index"))

if __name__=='__main__':
	app.run(debug=True)