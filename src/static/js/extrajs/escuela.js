(function( PerfilEscuela, $, undefined ) {
    var crear_comentario = function (url, id_validacion, comentario) {
        var data = {
            "id_validacion": id_validacion,
            "comentario": comentario
        }
        $.post(url, JSON.stringify(data)).then(function (response) {
            var fecha = new Date(response.fecha);
            var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear() + ", " + response.usuario);
            var td = $('<td></td>').text(response.comentario);
            var tr = $('<tr></tr>').append(td).append(td_data);
            $('#body-validacion-' + id_validacion).append(tr);
        }, function (response) {
            alert("Error al crear datos");
        });
    }
    var crear_comentario_solicitud = function (url, id_solicitud,comentario){
      var data = {
        "id_solicitud":id_solicitud,
        "comentario":comentario
      }
      $.post(url, JSON.stringify(data)).then(function (response){
        var fecha = new Date(response.fecha);
        var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear()+","+response.usuario);
        var td = $('<td></td>').text(response.comentario);
        var tr = $('<tr></tr>').append(td).append(td_data);
        $('#body-solicitud-' + id_solicitud).append(tr);
      },function(response){
        alert("Error al crear datos");
      });
    }

    var crear_monitoreo = function (url, comentario, equipamiento) {
        var data = {
            "comentario": comentario,
            "equipamiento": equipamiento
        }
        $.ajax({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            url: url,
            data: data,
            type: 'post',
            dataType: 'json',
            success: function (respuesta) {
                var fecha = new Date(respuesta.fecha);
                var fecha_text = fecha.getFullYear() + "-" + (fecha.getMonth()+1) + "-" + fecha.getDate();
                var btn = '<a href="'+respuesta.url+'" class="btn btn-xs btn-warning pull-right"><i class="fa fa-external-link p"></i></a>';
                var td_fecha = $('<td></td>').html(fecha_text+btn);
                var td_usuario = $('<td></td>').text(respuesta.creado_por);
                var td = $('<td></td>').text(respuesta.comentario);
                var tr = $('<tr></tr>').append(td).append(td_usuario).append(td_fecha);
                $('#body-monitoreo-' + respuesta.equipamiento).append(tr);
            }
        });
    }

    // Public
    PerfilEscuela.init = function () {
      /**/
      var visitas=[];
      var promedio=[];
      var ctx = document.getElementById('myChart');
      $.get($("#myChart").data('url'),{escuela:$("#semestre").data('codigo')},
          function (respuesta) {
             $.each(respuesta, function (index,datos) {
               visitas.push(datos.visita);
               promedio.push(datos.promedio);
              });
          });
      /*Inicio grafica*/


       var myChart = new Chart(ctx, {
         type: 'line',
               data: {
                 labels:visitas,
                 datasets: [{
                   label: 'visita',
                   backgroundColor: 'rgb(255, 99, 132)',
                   borderColor: 'rgb(255, 99, 132)',                   
                   fill: false,
                 }, {
                   label: 'promedio',
                   fill: false,
                   backgroundColor: 'rgb(54, 162, 235)',
                   borderColor: 'rgb(54, 162, 235)',
                   data: promedio,
                 }]
               },
               options: {
                 responsive: true,
                 title: {
                   display: true,
                   text: '¿ Promedio de las visitas realizadas a  escuelas'
                 },
                 tooltips: {
                   mode: 'index',
                   intersect: false,
                 },
                 hover: {
                   mode: 'nearest',
                   intersect: true
                 },
                 scales: {
                   xAxes: [{
                     display: true,
                     scaleLabel: {
                       display: true,
                       labelString: 'Visitas'
                     }
                   }],
                   yAxes: [{
                     display: true,
                     scaleLabel: {
                       display: true,
                       labelString: 'Promedio'
                     }
                   }]
                 }
               }
   });
      /*Fin graficas*/
      //aca comieza el  nuevo boton de impacto
      $('#btn-seguimiento').click(function () {
        bootbox.prompt({
            title: "Seleccione el semestre",
            inputType: 'select',
            inputOptions: [
            {
                text: '1',
                value: '1',
            },
            {
                text: '2',
                value: '2',
            }

            ],
            callback: function (result) {
              var escuela = $("#semestre").data('codigo');
              var url_visita = $("#semestre").data('url');
                $.ajax({
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                    },
                    url: url_visita,
                    data: {semestre:result,
                           escuela:escuela},
                    type: 'post',
                    success: function (respuesta) {
                      //location.href =$("#semestre").data('redirect');
                      window.open($("#semestre").data('redirect'), '_blank');

                    }
                });

            }
          });
      });
      //
        $('#form-nueva-solicitud').hide();
        $('#form-nuevo-equipamiento').hide();
        $('#btn-equipamiento').click(function () {
            $('#form-nuevo-equipamiento').toggle();
        });
        //aca comienza nuevo Formulario
        $('#form-nueva-visita').hide();
        $('#btn-equipamiento2').click(function () {
          $('#form-nueva-visita').toggle();
          //alert("Esto es un boton");
        });
        $('#form-nueva-validacion').hide();
        $('#form-nueva-visita-kalite').hide();
        $('#form-nueva-poblacion').hide();
        $('#form-nueva-matricula').hide();
        $('#btn-matricula').click(function () {
            $('#form-nueva-matricula').toggle();
        });
        $('#form-nuevo-rendimiento').hide();
        $('#btn-rendimiento').click(function () {
            $('#form-nuevo-rendimiento').toggle();
        });
        $('#btn-poblacion').click(function () {
            $('#form-nueva-poblacion').toggle();
        });
        $('.comentario-btn').click(function () {
            var id_validacion = $(this).data('id');
            var url = $(this).data('url');
            bootbox.prompt({
                title: "Nuevo registro",
                inputType: 'textarea',
                callback: function (result) {
                    if (result) {
                        crear_comentario(url, id_validacion, result);
                    }
                }
            });
        });

        $('.monitoreo-form').submit(function (e) {
            e.preventDefault();
            var url = $(this).prop('action');
            var equipamiento = $(this).data('equipamiento');
            bootbox.prompt({
                title: "Nuevo registro de monitoreo",
                inputType: 'textarea',
                callback: function (comentario) {
                    if (comentario) {
                        crear_monitoreo(url, comentario, equipamiento);
                    }
                }
            });
        });

      $('.comentarioSolicitud-btn').click(function (){
        var id_solicitud = $(this).data('id');
        var url = $(this).data('url');
        bootbox.prompt({
          title: "Nuevo Registro para Solicitud",
          inputType: 'textarea',
          callback: function (result){
            if(result){
              crear_comentario_solicitud(url, id_solicitud, result);
            }
          }
        });
      });
    }
}( window.PerfilEscuela = window.PerfilEscuela || {}, jQuery ));

(function( EscuelaBuscar, $, undefined ) {
    EscuelaBuscar.tablaHabilitada = false;
    EscuelaBuscar.tabla = null;
    EscuelaBuscar.filtro_list = [];
    EscuelaBuscar.iniciar_tabla = function () {
        let tabla = $('#escuela-table').DataTable({
            dom: 'lfrtipB',
            buttons: ['excel','pdf'],
            processing: true,
            deferLoading: 0,
            ajax: {
                url: $('#escuela-list-form').attr('action'),
                type: "POST",
                deferRender: true,
                dataSrc: '',
                data: function () {
                    return $('#escuela-list-form').serializeObject();
                }
            },
            preDrawCallback: function () {
                return EscuelaBuscar.tablaHabilitada;
            },
            columns: [
            {"data": "codigo", "class": "nowrap"},
            {
                data: "nombre",
                render: function ( data, type, full, meta ) {
                    return '<a href="' + full.escuela_url + '">' + data + '</a>';
                }
            },
            {"data": "direccion"},
            {"data": "departamento"},
            {"data": "municipio"},
            {"data": "sector"},
            {"data": "nivel"},
            {"data": "poblacion"},
            {
                data: "equipada",
                render: function (data) {
                    return data ? 'Sí' : 'No';
                }
            },
            {
                data: "capacitacion",
                render: function (data, type, full, meta) {
                    return data.capacitada ? 'Sí' : 'No';
                }
            },
            ]
        }).on('xhr.dt', function (e, settings, json, xhr) {
            $('#spinner').hide();
        });
        return tabla;
    }

    // Public
    EscuelaBuscar.init = function () {
        $('#spinner').hide();
        $('#escuela-list-form').submit(function (e) {
            // Evita que se envíe el formulario
            e.preventDefault();
            $('#spinner').show();

            EscuelaBuscar.filtro_list = [];

            if (EscuelaBuscar.tabla == null) {
                EscuelaBuscar.tabla = EscuelaBuscar.iniciar_tabla();
            }
            else{
                EscuelaBuscar.tabla.clear().draw();
            }
            $('#lista-filtros').empty();

            $("#escuela-list-form :input").not(':submit,:button,:hidden').each(function() {
                if($(this).val() != ""){
                    EscuelaBuscar.filtro_list.push($("label[for='"+$(this).attr('id')+"']").text());
                }
            });

            if (EscuelaBuscar.filtro_list.length > 0) {
                EscuelaBuscar.tablaHabilitada = true;
                $('#filtros-collapse').hide();
                $('#spinner').show();
                EscuelaBuscar.tabla.clear().draw();
                EscuelaBuscar.tabla.ajax.reload();
            }
            else{
                EscuelaBuscar.tablaHabilitada = false;
                $('#lista-filtros').append('<li>Seleccione al menos un filtro</li>');
                $('#filtros-collapse').show();
                $('#spinner').hide();
            }
        });
        $('#escuela-list-form #id_departamento').on('change', function () {
            listar_municipio_departamento('#escuela-list-form #id_departamento', '#escuela-list-form #id_municipio', true);
        });
    }
}( window.EscuelaBuscar = window.EscuelaBuscar || {}, jQuery ));

(function( EscuelaContacto, $, undefined ) {
    // Public
    EscuelaContacto.init = function () {

    }
}( window.EscuelaContacto = window.EscuelaContacto || {}, jQuery ));
