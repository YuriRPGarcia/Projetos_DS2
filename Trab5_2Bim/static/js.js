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