class Recaudacion {
  constructor() {
    var tabla = $('#proveedores-recaudacion-table').DataTable({
        dom: 'Bfrtip',
        buttons: ['excel', 'pdf', 'copy'],
        processing: true,
        ajax: {
            url: $('#proveedores-recaudacion-table').data('url'),
            deferRender: true,
            dataSrc: '',
            cache: true,
        },
        columns: [
            {data: "nombre"},
            {data: "cantidad"},
            {data: "entradas"},
        ]
    });
    $("#contactForm").submit(function(event){
 	    submitForm();
 		  return false;
 	});
   /*funcion para manejar Ajax*/
   function submitForm(){
	 $.ajax({
     beforeSend: function(xhr, settings) {
         xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
     },
		type: "POST",
		url:  $('#proveedores-recaudacion-table').data('url') + "crear_proveedor/",
		cache:false,
		data: $('form#contactForm').serialize(),
		success: function(response){
      bootbox.alert(response.mensaje, function (){
        document.getElementById("contactForm").reset();
        $("#contact").html(response)
        $("#contact-modal").modal('hide');
        location.reload();
      });
		},
		error: function(){
      bootbox.alert(response["mensaje"]);
		}
	});
}
  }
}

class Entrada {
  constructor() {
    $('#terminar-entrada-recaudacion').click(function () {
        bootbox.confirm({
            message: "¿Está seguro que quiere dar por finalizada la edición de la entrada?",
            buttons: {
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirmar',
                    className: 'btn-success'
                },
                cancel: {
                    label: '<i class="fa fa-times"></i> Cancelar',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result == true) {
                  $.ajax({
                    type: "POST",
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                    },
                    dataType: 'json',
                    data: {
                      id:$('#terminar-entrada-recaudacion').data("pk"),
                    },
                    url: $('#terminar-entrada-recaudacion').data("url")+"cerrar_entrada/",
                    success: function (response) {
                         bootbox.alert({message: "<h2>"+response.mensaje+"</h2>", className:"modal modal-success fade in"});
                         location.reload();

                    },
                    error: function (response) {
                      var mensaje = JSON.parse(response.responseText)
                      bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
                    }
                });

                }

            }
        });


    });
    /**Busqueda de entrada**/
    $('#entrada-buscar-form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                url: $(this).prop('action'),
                data: {
                    id: $('#entrada-buscar-form #entrada-id').val()
                },
                success: function (respuesta) {
                    if (respuesta.length > 0) {
                        window.location = respuesta[0].url;
                    }
                }
            });
        });
        /*filtros de busqueda*/
        $('#filter-form').submit(function (e) {
            e.preventDefault();
            $('#tbody-entradas').empty();
            $.ajax({
                url: $(this).prop('action'),
                data: $(this).serializeObject(),
                success: function (respuesta) {
                    var tr = '';
                    $.each(respuesta, function (index, entrada) {
                        tr = '<td><a href="'+entrada.url+'" class="btn btn-block">'+entrada.id+'</a></td>';
                        tr += '<td>'+entrada.proveedor+'</td>';
                        tr += '<td nowrap>'+entrada.fecha+'</td>';
                        $('#tbody-entradas').append('<tr>'+tr+'</tr>');
                    })
                }
            });
        });
  }
}
class Articulo {
  constructor() {
    var tabla = $('#articulos-recaudacion-table').DataTable({
        dom: 'Bfrtip',
        buttons: ['excel', 'pdf', 'copy'],
        processing: true,
        ajax: {
            url: $('#articulos-recaudacion-table').data('url'),
            deferRender: true,
            dataSrc: '',
            cache: true,
        },
        columns: [
            {data: "nombre"},
            {data: "categoria"},
            {data: "precio"},
            {data: "entrada"},
            {data: "salidas"},
            {data: "existencia"},
        ]
    });
    $('#articulos-recaudacion-table tbody').on('click', 'tr', function () {
          var data = tabla.row( this ).data();
          entrada_articulos(data.id);
          salidas_articulos(data.id);
      } );
 function entrada_articulos(id) {
   var tabla_entrada = $('#entrada-articulos-table').DataTable({
       dom: 'Bfrtip',
       buttons: ['excel', 'pdf', 'copy'],
       processing: true,
       ajax: {
           url: $('#entrada-articulos-table').data('url'),
           deferRender: true,
           dataSrc: '',
           cache: true,
           data: function (params)
           {
              return {
                articulo: id
              };
           }
       },
       columns: [
           {data: "entrada_id"},
           {data: "proveedor"},
           {data: "fecha"},
           {data: "cantidad"},
           {data: "tarima"},
           {data: "caja"},
       ]
   });

 }
 function salidas_articulos(id) {
   var tabla_salida = $('#salidas-articulos-table').DataTable({
       dom: 'Bfrtip',
       buttons: ['excel', 'pdf', 'copy'],
       processing: true,
       ajax: {
           url: $('#salidas-articulos-table').data('url'),
           deferRender: true,
           dataSrc: '',
           cache: true,
           data: function (params)
           {
              return {
                articulo: id
              };
           }
       },
       columns: [
           {data: "salida_id"},
           {data: "tipo"},
           {data: "fecha"},
           {data: "cantidad"},
           {data: "total_salida"},
       ]
   });

 }


  }
}
class Salida {
  constructor() {
    $('#id_articulo').change( function() {
      var selected_valor_articulo = $('#id_articulo option:selected').val();
      $.ajax({
        url:$('#detalle-form').data('url'),
        dataType:'json',
        data:{
          id:selected_valor_articulo
        },
        error:function(){
          console.log("Error");
        },
        success:function(data){
          if(data[0].existencia == 0){
             bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + "Ya no hay disponibilidad del articulo", className:"modal modal-danger fade"});
             $('#boton-agregar').prop('disabled', true);
             $('#id_precio').val(data[0].precio);
             $('#id_cantidad').val(data[0].existencia);
         }else{
             $('#id_precio').val(data[0].precio);
             $('#id_cantidad').val(data[0].existencia);
               $('#boton-agregar').prop('disabled', false);
         }

        },
        type: 'GET'
      }
    );
    });

    /**/
    /**Busqueda de entrada**/
    $('#salida-buscar-form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                url: $(this).prop('action'),
                data: {
                    id: $('#salida-buscar-form #salida-id').val()
                },
                success: function (respuesta) {
                    if (respuesta.length > 0) {
                        window.location = respuesta[0].url;
                    }
                }
            });
        });
        /**/
        /*filtros de busqueda*/
        $('#filter-form-salidas').submit(function (e) {
            e.preventDefault();
            $('#tbody-salidas').empty();
            $.ajax({
                url: $(this).prop('action'),
                data: $(this).serializeObject(),
                success: function (respuesta) {
                    var tr = '';
                    $.each(respuesta, function (index, salida) {
                        tr = '<td><a href="'+salida.url+'" class="btn btn-block">'+salida.id+'</a></td>';
                        tr += '<td>'+salida.tipo+'</td>';
                        tr += '<td nowrap>'+salida.fecha+'</td>';
                        $('#tbody-salidas').append('<tr>'+tr+'</tr>');
                    })
                }
            });
        });
        /**/
        $('#terminar-salida-recaudacion').click(function () {
            bootbox.confirm({
                message: "¿Está seguro que quiere dar por finalizada la edición de la salida?",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirmar',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancelar',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result == true) {
                      $.ajax({
                        type: "POST",
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                        },
                        dataType: 'json',
                        data: {
                          id:$('#terminar-salida-recaudacion').data("pk"),
                        },
                        url: $('#terminar-salida-recaudacion').data("url")+"cerrar_salida/",
                        success: function (response) {
                             bootbox.alert({message: "<h2>"+response.mensaje+"</h2>", className:"modal modal-success fade in"});
                             location.reload();
                        },
                        error: function (response) {
                          var mensaje = JSON.parse(response.responseText)
                          bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
                        }
                    });

                    }

                }
            });


        });

  }
}
