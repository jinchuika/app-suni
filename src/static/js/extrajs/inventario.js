(function( EnCreacion, $, undefined ) {
  EnCreacion.init = function () {
    var mensaje = document.getElementById("id_en_creacion");
    $('#id_en_creacion').click(function(){
      if($("#id_en_creacion").is(':checked')){
        bootbox.alert("esta activado");
      }else {
        bootbox.alert("Esta Seguro que quiere Terminara la Creacion de la Entrada");
      }
    });


  }

}(window.EnCreacion = window.EnCreacion || {}, jQuery ));

(function(DetalleList, $, undefined){
  var valor = $('#entrada-table').data("api");
  var pk = $('#entrada-table').data("pk");
  var urlapi = valor + "?entrada="+ pk;
  /***/
  var tabla = $('#entrada-table').DataTable( {
    searching: false,
    paging: false,
    ordering:  false,
    processing: true,
    ajax:{
      url:urlapi,
      dataSrc: '',
      cache:true,
      data: function () {
        var cont = $('#entrada-table').data("api");
          return cont;
      }
    },
    columns:[
      {data:"tdispositivo"},
      {data:"util"},
      {data:"repuesto"},
      {data:"desecho"},
      {data:"total"},
      {data:"precio_unitario"},
      {data:"precio_subtotal"},
      {data:"precio_descontado"},
      {data:"precio_total"},
      {data:"creado_por"}

    ]
  });

  DetalleList.init = function() {
    /** Uso de DRF**/
    $('#detalleForm').submit( function (e){
    e.preventDefault()

     $.ajax({
        type: 'POST',
        url: $('#detalleForm').attr('action'),
        data:$('#detalleForm').serialize(),
        success: function (response) {
          console.log("datos ingresados correctamente");

        },
      });
      tabla.clear().draw();
      tabla.ajax.reload();
      document.getElementById("detalleForm").reset();
    });





  }
}(window.DetalleList =  window.DetalleList || {}, jQuery));
