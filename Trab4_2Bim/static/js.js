function validaEmpresa(frm) {
           
  if (isNaN(this.cnpj.value)) {
    alert("digite apenas numeros!");
    this.cnpj.select();
    return false;
  }else{
    c = this.cnpj.value;
  }
  if (c.toString().length != 14) {
    alert("o cnpj tem de ter 14 numeros!");
    this.cnpj.select();
    return false;
  }
  
  n = this.nome.value;
  if (n.toString().length > 100) {
    alert("O nome é muito grande");
    this.nome.select();
    return false;
  }
  
  s = this.senha.value;
  if (s.toString().length > 100) {
    alert("A senha é muito grande");
    this.senha.select();
    return false;
  }
  
  l = this.logo.value;
  if (l.toString().length > 100) {
    alert("O nome do arquivo é muito grande");
    this.foto.select();
    return false;
  }

}

function validaAluno(frm) {
  if (isNaN(this.matricula.value)) {
    alert("digite apenas numeros!");
    this.matricula.select();
    return false;
  }else{
    mat = this.matricula.value;
  }
  if (mat.toString().length != 8) {
    alert("a matricula tem de ter 8 numeros!");
    this.matricula.select();
    return false;
  }

  n = this.nome.value;
  if (n.toString().length > 100) {
    alert("O nome é muito grande");
    this.nome.select();
    return false;
  }

  s = this.senha.value;
  if (s.toString().length > 100) {
    alert("A senha é muito grande");
    this.senha.select();
    return false;
  }
  
  f = this.foto.value;
    if (f.toString().length > 100) {
    alert("O nome do arquivo é muito grande");
    this.foto.select();
    return false;
    }
}

$(document).ready(function(){
  $('.datepicker').datepicker(); 
});

$(document).ready(function(){
  $('select').formSelect();
});