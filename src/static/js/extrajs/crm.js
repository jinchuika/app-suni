(function( HistoricoOfertas, $, undefined ) {
    var crear_historial_ofertas = function (url, id_solicitud, comentario){
      var data = {
        "id_historico":id_solicitud,
        "comentario":comentario
      }
      console.log(comentario)
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
