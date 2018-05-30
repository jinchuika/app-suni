(function( AlertaEnCreacion, $, undefined ) {
  AlertaEnCreacion.init = function () {
    var mensaje = document.getElementById("id_en_creacion");
    $('#id_en_creacion').click(function(){
      if($("#id_en_creacion").is(':checked')){
        bootbox.alert("esta activado");
      }else {
        bootbox.alert("Esta Seguro que quiere Terminara la Creacion de la Entrada");
      }
    });


  }

}(window.AlertaEnCreacion = window.AlertaEnCreacion || {}, jQuery ));

(function(EntradaDetalleList, $, undefined){
  var valor = $('#entrada-table').data("api");
  var pk = $('#entrada-table').data("pk");
  var urlapi = valor + "?entrada="+ pk;
  var tabla = $('#entrada-table').DataTable( {
    searching: false,
    paging: true,
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
      {data:"creado_por"},
      {data:"",defaultContent:"<button class='btn btn-info'>Editar</button>",targets: -1},
      {data:"",defaultContent:"<button class='btn btn-primary'>Crear Disp</button>",targets: -1},



    ]
  });

  EntradaDetalleList.init = function() {
  $('#entrada-table tbody').on( 'click', '.btn-info', function () {
       var data = tabla.row( $(this).parents('tr') ).data();
       location.href =data.update_url;
   } );

   $('#entrada-table tbody').on( 'click', '.btn-primary', function () {
         var data = tabla.row( $(this).parents('tr') ).data();
        var valordispositivo = $('#entrada-table').data("api");
        var urldispositivo = valor +data.id+"/crear_dispositivos/";
         console.log(urldispositivo);
        $.ajax({
           type: 'POST',
           url:urldispositivo,
           data: {csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
           success: function(response){
             console.log("dispositivos creados exitosamente");
           },

         });
    } );
    /** Uso de DRF**/
    $('#detalleForm').submit( function (e){
    e.preventDefault()

     $.ajax({
        type: "POST",
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
}(window.EntradaDetalleList =  window.EntradaDetalleList || {}, jQuery));

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

        {data:"tipo"},
        {data:"fecha",className:"nowrap"},
        {data:"en_creacion",className:"nowrap"},
        {data:"creada_por",className:"nowrap"},
        {data:"recibida_por",className:"nowrap"},
        {data:"proveedor", className:"nowrap"},
        {data:"",defaultContent:"<button>Edit</button>",targets: -1}
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

      $('#entrada2-table tbody').on( 'click', 'button', function () {
         var data = tabla.row( $(this).parents('tr') ).data();
         alert("Si funciona este boton");
         console.log(data.fecha);
     } );

  }
}( window.EntradaList = window.EntradaList || {}, jQuery ));

(function(SalidaDetalleList, $, undefined){
  var valor = $('#salida-table').data("api");
  var pk = $('#salida-table').data("pk");
  var urlapi = valor + "?entrada="+ pk;
  var tabla = $('#salida-table').DataTable( {
    searching: false,
    paging: true,
    ordering:  false,
    processing: true,
    ajax:{
      url:urlapi,
      dataSrc: '',
      cache:true,
      data: function () {
        var cont = $('#salida-table').data("api");
          return cont;
      }
    },
    columns:[
      {data:"tdispositivo"},
      {data:"cantidad"},
      {data:"desecho"},
      {data:"entrada_detalle"},
    ]
  });

  SalidaDetalleList.init = function() {
    $('#btn-terminar').click(function(){
      bootbox.alert("Esta Seguro que quiere Terminara la Creacion de la Entrada");
      document.getElementById("id_en_creacion").checked = false;
      document.getElementById("desechosalida-form").submit()
      });

    /** Uso de DRF**/
    $('#detalleForm').submit( function (e){
    e.preventDefault()

     $.ajax({
        type: "POST",
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
}(window.SalidaDetalleList =  window.SalidaDetalleList || {}, jQuery));
