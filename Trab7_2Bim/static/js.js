function cadastraEmail() {
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (req.readyState == 4){
      if (req.status == 200){
        var response = JSON.parse(req.responseText);
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = response.mensagem;
      }
    }
  }
  req.open('POST', '/email');
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var email = document.getElementById('email').value;
  var postVars = 'email='+email;
  req.send(postVars);        
  return false;
}

function loadAssunto() {
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (req.readyState == 4){
      if (req.status == 200){
        var response = JSON.parse(req.responseText);
        var assunto = document.createElement('a');
        assunto.href = '/noticia_assunto/'+response.id;
        assunto.innerHTML = response.nome;
        assunto.className = "collection-item";
        document.getElementById('assuntos').appendChild(assunto);
      }
    }
  }
  req.open('POST', '/administracao/cadastrar_assunto');
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var nome = document.getElementById('nome').value;
  var postVars = 'nome='+nome;
  req.send(postVars);        
  return false;
}

function fechaTudo(){
  var n = document.getElementById('noticias');
  while (n.firstChild) n.removeChild(n.firstChild);
}

function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

var myEfficientFn = debounce(function() {
  var n = document.getElementById('noticias');
  while (n.firstChild) n.removeChild(n.firstChild);
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (req.readyState == 4){
      if (req.status == 200){
        var response = JSON.parse(req.responseText);
        var noticia;
        for (var i = 0; i < response.vetNoticia.length; i++) {
          var noticia = document.createElement('a');
          var aux = response.vetNoticia[i].split(";")
          noticia.href = '/noticia/'+aux[0];
          noticia.innerHTML = aux[1];
          noticia.className = "collection-item";
          document.getElementById('noticias').appendChild(noticia);
        }
      }
    }
  }
  req.open('POST', '/busca_autoComplete');
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var busca = document.getElementById('busca').value;
  var postVars = 'busca='+busca;
  req.send(postVars);        
  return false;
}, 250);

window.addEventListener('keyup', myEfficientFn);


var check = function() {
  if (document.getElementById('senha').value == document.getElementById('confirma_senha').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'Senhas são iguais';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'Senhas não são iguais';
  }
}

$(document).ready(function(){
   $("[name='mostraForm']").click(function(e) {
        $("[name='formAssunto']").show();
        e.preventDefault();
    });
});

$(document).ready(function(){
	$('select').formSelect();
});

function validaNoticia(frm){
  if(this.titulo.value.toString().length >1000 || this.texto.value.toString().length > 10000 || this.foto.value.toString().length > 100){
    return false;
  }
}

function validaAssunto(frm){
  if(this.nome.value.toString().length >100){
    return false;
  }
}

function validaPessoa(frm){
  
  if(this.login.value.toString().length > 100 || this.senha.value.toString().length > 100 || this.nome.value.toString().length > 100){
    return false;
  }else if(this.senha.value.toString().length != this.confirma_senha.value.toString().length){
    return false;
  }else{
    return true;
  }
}

function validaComentario(frm){
  if(this.texto.value.toString().length > 1000){
    return false;
  }
}