(function( EnCreacion, $, undefined ) {
  EnCreacion.init = function () {
    var mensaje = document.getElementById("id_en_creacion");
    $('#id_en_creacion').click(function(){
      if($("#id_en_creacion").is(':checked')){
        bootbox.alert("esta activado");
      }else {
        bootbox.alert("No esta activado");
      }
    });


  }

}(window.EnCreacion = window.EnCreacion || {}, jQuery ));
