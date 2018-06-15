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
   $("#mostraForm").click(function(e) {
        $("#formAssunto").show();
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