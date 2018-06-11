# importando a biblioteca flask
from flask import Flask
# habilitando o redirecionamento
from flask import abort, redirect, url_for
# importando a camada de persistencia, ou seja, os daos
from persistencia import *
# templates
from flask import render_template
# receber dados do formulario
from flask import request

# criando um objeto de Flask
app = Flask(__name__)

# definindo a rota index
@app.route('/')
def index():	
    return render_template("index.html")

@app.route('/gerenciar_filmes')
def gerenciar_filmes():	
    return render_template("gerenciar_filmes.html")

@app.route('/gerenciar_sessoes')
def gerenciar_sessoes():	
    return render_template("gerenciar_sessoes.html")

@app.route('/gerenciar_ingressos')
def gerenciar_ingressos():	
    return render_template("gerenciar_ingressos.html")




# rotas relacionadas a filme
@app.route('/tela_cadastrar_filme')
def tela_cadastrar_filme():	
    return render_template("tela_cadastrar_filme.html")

@app.route('/cadastrar_filme', methods=['POST'])
def cadastrar_filme():	
	filme = Filme()
	filme.titulo = str(request.form['titulo'])
	filme.sinopse = str(request.form['sinopse'])
	filme.genero = str(request.form['genero'])
	filme.foto = str(request.form['foto'])
	filme.dataInicio = str(request.form['dataInicio'])
	filme.dataFim = str(request.form['dataFim'])
	filmeDAO = FilmeDAO()
	filmeDAO.adicionar(filme)
	return redirect(url_for("listar_filmes"))

@app.route('/tela_alterar_filme/<cod>')
def tela_alterar_filme(cod):	
    return render_template("tela_alterar_filme.html", filme = FilmeDAO().obter(int(cod)))

@app.route('/alterar_filme', methods=['POST'])
def alterar_filme():	
	filme = Filme()
	filme.cod = int(request.form['cod'])
	filme.titulo = str(request.form['titulo'])
	filme.sinopse = str(request.form['sinopse'])
	filme.genero = str(request.form['genero'])
	filme.foto = str(request.form['foto'])
	filme.dataInicio = str(request.form['dataInicio'])
	filme.dataFim = str(request.form['dataFim'])
	filmeDAO = FilmeDAO()
	filmeDAO.alterar(filme)
	return redirect(url_for("alterar_filmes"))

@app.route("/excluir_filme/<cod>")
def excluir_filme(cod):
	filmeDAO = FilmeDAO()
	filmeDAO.excluir(int(cod))
	return redirect(url_for('excluir_filmes'))

@app.route("/listar_filmes")
def listar_filmes():
	filmeDAO = FilmeDAO()
	return render_template("listar_filmes.html", vetFilmes = filmeDAO.listar())

@app.route("/excluir_filmes")
def excluir_filmes():
	filmeDAO = FilmeDAO()
	return render_template("excluir_filmes.html", vetFilmes = filmeDAO.listar())

@app.route("/alterar_filmes")
def alterar_filmes():
	filmeDAO = FilmeDAO()
	return render_template("alterar_filmes.html", vetFilmes = filmeDAO.listar())




# rotas relacionadas a sessao
@app.route('/tela_cadastrar_sessao/<cod>')
def tela_cadastrar_sessao(cod):	
    return render_template("tela_cadastrar_sessao.html", filme = FilmeDAO().obter(int(cod)))

@app.route('/cadastrar_sessao', methods=['POST'])
def cadastrar_sessao():	
	sessao = Sessao()
	sessao.codFilme = int(request.form['codFilme'])
	sessao.dia = str(request.form['dia'])
	sessao.hora = str(request.form['hora'])
	sessaoDAO = SessaoDAO()
	sessaoDAO.adicionar(sessao)
	return redirect(url_for("gerenciar_sessoes"))

@app.route('/tela_alterar_sessao/<cod>')
def tela_alterar_sessao(cod):	
    return render_template("tela_alterar_sessao.html", sessao = SessaoDAO().obter(int(cod)))

@app.route('/alterar_sessao', methods=['POST'])
def alterar_sessao():	
	sessao = Sessao()
	sessao.cod = int(request.form['cod'])
	sessao.codFilme = int(request.form['codFilme'])
	sessao.dia = str(request.form['dia'])
	sessao.hora = str(request.form['hora'])
	sessaoDAO = SessaoDAO()
	sessaoDAO.alterar(sessao)
	return redirect(url_for("gerenciar_sessoes"))

@app.route("/excluir_sessao/<cod>")
def excluir_sessao(cod):
	sessaoDAO = SessaoDAO()
	sessaoDAO.excluir(int(cod))
	return redirect(url_for('gerenciar_sessoes'))

@app.route("/listar_sessoes/<codFilme>")
def listar_sessoes(codFilme):
	return render_template("listar_sessoes.html", vetSessoes = SessaoDAO().listar(codFilme))

@app.route('/escolher_filme_listar')
def escolher_filme_listar():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme_listar.html", vetFilmes = filmeDAO.listar())

@app.route('/escolher_filme_excluir')
def escolher_filme_excluir():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme_excluir.html", vetFilmes = filmeDAO.listar())

@app.route('/escolher_filme_alterar')
def escolher_filme_alterar():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme_alterar.html", vetFilmes = filmeDAO.listar())

@app.route("/excluir_sessoes/<codFilme>")
def excluir_sessoes(codFilme):
	return render_template("excluir_sessoes.html", vetSessoes = SessaoDAO().listar(codFilme))

@app.route("/alterar_sessoes/<codFilme>")
def editar_sessoes(codFilme):
	return render_template("alterar_sessoes.html", vetSessoes = SessaoDAO().listar(codFilme))

@app.route('/escolher_filme_cadastrar')
def escolher_filme_cadastrar():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme_cadastrar.html", vetFilmes = filmeDAO.listar())





# rotas relacionadas a ingresso
@app.route('/tela_comprar_ingresso/<codSessao>')
def tela_comprar_ingresso(codSessao):	
    return render_template("tela_comprar_ingresso.html", sessao = SessaoDAO().obter(int(codSessao)), vetIngressos = IngressoDAO().listar(codSessao))

@app.route('/comprar_ingresso', methods=['POST'])
def comprar_ingresso():
	ingresso = Ingresso()
	ingresso.nomeCliente = str(request.form['nomeCliente'])
	ingresso.cadeira = int(request.form['cadeira'])
	ingresso.codSessao = int(request.form['codSessao'])
	ingressoDAO = IngressoDAO()
	ingressoDAO.adicionar(ingresso)
	return redirect(url_for("gerenciar_ingressos"))

@app.route('/tela_alterar_ingresso/<cod>')
def tela_alterar_ingresso(cod):	
    return render_template("tela_alterar_ingresso.html", ingresso = IngressoDAO().obter(int(cod)))

@app.route('/alterar_ingresso', methods=['POST'])
def alterar_ingresso():	
	ingresso = Ingresso()
	ingresso.nomeCliente = str(request.form['nomeCliente'])
	ingressoDAO = IngressoDAO()
	ingressoDAO.alterar(ingresso)
	return redirect(url_for("gerenciar_ingressos"))

@app.route("/excluir_ingresso/<cod>")
def excluir_ingresso(cod):
	ingressoDAO = IngressoDAO()
	ingressoDAO.excluir(int(cod))
	return redirect(url_for('gerenciar_ingressos'))

@app.route('/escolher_filme')
def escolher_filme():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme.html", vetFilmes = filmeDAO.listar())

@app.route("/escolher_sessao/<codFilme>")
def escolher_sessao(codFilme):
	return render_template("escolher_sessao.html", vetSessoes = SessaoDAO().listar(codFilme))

@app.route('/escolher_filme_listar_sessoes')
def escolher_filme_listar_sessoes():	
	filmeDAO = FilmeDAO()
	return render_template("escolher_filme_listar_sessoes.html", vetFilmes = filmeDAO.listar())

@app.route('/escolher_sessao_listar_ingressos<codFilme>')
def escolher_sessao_listar_ingressos(codFilme):	
	filmeDAO = FilmeDAO()
	return render_template("escolher_sessao_listar_ingressos.html", vetSessoes = SessaoDAO().listar(codFilme))

@app.route('/listar_ingressos<codSessao>')
def listar_ingressos(codSessao):	
	filmeDAO = FilmeDAO()
	return render_template("listar_ingressos.html", vetIngressos = IngressosDAO().listar(codSessao))





# Como executa?

# Opcoes:

# 1) No terminal
# python main.py

# 2) No terminal:
# FLASK_APP=main.py FLASK_DEBUG=1 flask run

# Traduzindo o comando....
# Estou executando o arquivo main.py
# habilitei o debug

# startando....
if __name__ == '__main__':
	app.run(debug=True)