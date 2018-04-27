(function( HistoricoOfertas, $, undefined ) {
    var crear_historial_ofertas = function (url, id_solicitud, comentario){
      var data = {
        "id_historico":id_solicitud,
        "comentario":comentario
      }
      console.log(id_solicitud);
      $.post(url, JSON.stringify(data)).then(function (response){
        var fecha = new Date(response.fecha);
        var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear()+","+response.usuario);
        var td = $('<td></td>').text(response.comentario);
        var tr = $('<tr></tr>').append(td).append(td_data);
      $('#body-historial-' + id_solicitud).append(tr);

      },function(response){
        alert("Error al crear datos");
      });
    }


    // Public
    HistoricoOfertas.init = function () {
      $('.ofertaHistorico-btn').click(function (){
        var id_solicitud = $(this).data('id');
        var url = $(this).data('url');
        bootbox.prompt({
          title: "Historial de Ofertas",
          inputType: 'textarea',
          callback: function (result) {
            if (result) {
              crear_historial_ofertas(url, id_solicitud, result);

            }
          }
        });
      });
    }
}( window.HistoricoOfertas = window.HistoricoOfertas || {}, jQuery ));

(function( OfertasList, $, undefined ) {
    var tabla = $('#ofertas-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#ofertas-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            cache:true,
            data: function () {
                return $('#ofertas-list-form').serializeObject(true);
            }
        },
        columns: [
          {data:"id",
          render: function(data, type, full, meta){
            return '<a href="'+full.url+'">'+data +'</a>'
          }},
          {data:"fecha_inicio",className:"nowrap"},
          {data:"donante",
          className:"nowrap",
          render:function(data, type, full, meta){
            return '<a href="'+full.urlDonante+'">'+data+'</a>'
          }},
          {data:"recibido",className:"nowrap"},
          {data:"fecha_bodega",className:"nowrap"},
          {data:"tipo_oferta",className:"nowrap"},
          {data:"fecha_carta", className:"nowrap"},
          {data:"contable", className:"nowrap"}

        ]

    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    OfertasList.init = function () {
        $('#spinner').hide();
        $('#ofertas-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
    }
}( window.OfertasList = window.OfertasList || {}, jQuery ));
