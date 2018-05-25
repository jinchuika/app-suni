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
/****/
(function( EntradaList, $, undefined ) {
 var tabla = $('#entrada2-table').DataTable({
      dom: 'lfrtipB',
      buttons: ['excel','pdf'],
      processing: true,
      ajax: {
          url: $('#entrada2-list-form').attr('action'),
          deferRender: true,
          dataSrc: '',
          cache:true,
          data: function () {
              return $('#entrada2-list-form').serializeObject(true);
          }
      },
      columns: [
        {data:"tipo",className:"nowrap"},
        {data:"fecha",className:"nowrap"},
        {data:"en_creacion",className:"nowrap"},
        {data:"creada_por",className:"nowrap"},
        {data:"recibida_por",className:"nowrap"},
        {data:"proveedor", className:"nowrap"}

      ]

  }).on('xhr.dt', function (e, settings, json, xhr) {
      $('#spinner').hide();
  });

  EntradaList.init = function () {
      $('#spinner').hide();
      $('#entrada2-list-form').submit(function (e) {
          e.preventDefault();
          $('#spinner').show();
          tabla.clear().draw();
          tabla.ajax.reload();
      });
  }
}( window.EntradaList = window.EntradaList || {}, jQuery ));
