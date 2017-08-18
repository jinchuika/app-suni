function listar_grupos_sede(sede_selector, grupo_selector, null_option) {
    /*
    Al cambiar la sede, genera el listado de grupos
    */
    $(grupo_selector).html('');
    if ($(sede_selector).val()) {
        $.get($(sede_selector).data('url'),
        {
            sede: $(sede_selector).val()
        },
        function (respuesta) {
            var options = '';
            if (null_option) {
                options += '<option value="">------</option>';
            }
            $.each(respuesta, function (index, grupo) {
                options += '<option value="'+grupo.id+'">'+grupo.numero+' - '+grupo.curso+'</option>';
            });
            $(grupo_selector).html(options).trigger('change');
        });
    }
}

function validar_udi_api(params) {
    if(validar_udi(params.udi)){
        $.get(params.url,
        {
            codigo: params.udi,
            fields: 'nombre'
        }, function (respuesta) {
            params.callback(respuesta);
        });
    }
}

(function( BuscadorSede, $, undefined ) {
    BuscadorSede.init = function () {
        var options = {
            valueNames: [ 'sede', 'capacitador']
        };
        var userList = new List('buscador', options);
        
        $('#id_capacitador').change(function () {
            var tr = $('.tr-sede');
            if ($(this).val() == '') {
                $(tr).show();
                return false;
            }
            for (var i = 0; i < tr.length; i++) {
                if($(tr[i]).data('capacitador-id') == $(this).val()) {
                    $(tr[i]).show();
                }
                else{
                    $(tr[i]).hide();
                }
            }
        })

    }
}( window.BuscadorSede = window.BuscadorSede || {}, jQuery ));

(function( SedeDetail, $, undefined ) {
    var crear_celda = function (asesoria) {
        var fila = $('<tr />');
        fila.append('<td><a href="#" class="editable" data-name="fecha" data-type="text" data-pk="'+asesoria.id+'" data-url="'+asesoria.url+'">' + asesoria.fecha + '</a></td>');
        fila.append('<td><a href="#" class="editable" data-name="hora_inicio" data-type="text" data-pk="'+asesoria.id+'" data-url="'+asesoria.url+'">' + asesoria.hora_inicio + '</a></td>');
        fila.append('<td><a href="#" class="editable" data-name="hora_fin" data-type="text" data-pk="'+asesoria.id+'" data-url="'+asesoria.url+'">' + asesoria.hora_fin + '</a></td>');
        fila.append('<td><a href="#" class="editable" data-name="observacion" data-type="text" data-pk="'+asesoria.id+'" data-url="'+asesoria.url+'">' + asesoria.observacion + '</a></td>');
        $('#asesoria-tabla-body').append(fila);
        activar_edicion();
    }

    var activar_edicion = function () {
        $('.editable').on('shown', function(e, editable) {
            $('.datepicker').datepicker({
                format: 'yyyy-mm-dd',
                autoclose: true,
                language: 'es'
            });
        }).editable({
            ajaxOptions: {
                contentType: 'application/json',
                dataType: 'json',
                type: "PATCH",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                }
            },
            params: function(params) {
                var obj = {};
                obj[params['name']] = params['value'];
                return JSON.stringify(obj);
            }
        });
    }
    
    SedeDetail.init = function () {
        activar_edicion();
        $('#asesoria-form').hide();
        $('#btn-asesoria').on('click', function () {
            $('#asesoria-form').toggle();
        });
        $('#asesoria-form').on('submit', function (e) {
            e.preventDefault();
            $.post($(this).attr('action'), $(this).serializeObject(), function (respuesta) {
                $('#asesoria-form')[0].reset();
                $('#asesoria-form').hide();
                crear_celda(respuesta);
            });
        });

        $('.eliminar-asesoria').on('click', function () {
            var boton = $(this);
            bootbox.confirm('¿Desea eliminar el período de asesoría?', function (result) {
                if(result){
                    $.ajax({
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
                        },
                        success: function (respuesta) {
                            $('#asesoria-'+boton.data('pk')).remove();
                        },
                        dataType: 'json',
                        type: 'DELETE',
                        url: boton.data('url')
                    });
                }
            });
        });
    }
}( window.SedeDetail = window.SedeDetail || {}, jQuery ));


(function( GrupoDetail, $, undefined ) {
    var crear_grafico = function (contenedor) {
        var url = $(contenedor).data('url');
        var grupo_id = $(contenedor).data('grupo_id');

        $.get(url, {grupo: grupo_id, fields: 'cr_asistencia,asistentes'}, function (respuesta) {
            var asistencias_chart = new Chart(contenedor, {
                type: 'line',
                data: {
                    labels: respuesta.map(function (calendario) {return calendario.cr_asistencia}),
                    datasets: [{
                        label: "Asistentes",
                        data: respuesta.map(function (calendario) {return calendario.asistentes}),
                        borderColor: "#3e95cd",
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                beginAtZero:true
                            },
                            scaleSteps : 10,
                        }]
                    }
                }
            });
        })
    }

    var copiar_participantes = function () {
        var api_url = $('#copiar-form').prop('action');
        var grupo_id = $('#copiar-form #id_grupo').val();
        var total = $('.check-participante:checkbox:checked').length;
        var completados = 0;
        $('.check-participante:checkbox:checked').each(function () {
            var participante_id = $(this).val();
            $.ajax({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                },
                data: {
                    grupo: grupo_id,
                    participante: participante_id
                },
                dataType: 'json',
                error: function (respuesta) {
                    completados += 1;
                    new Noty({
                        text: 'Error al asignar a ' + $('#td-nombre-'+participante_id).text() + ' ' + $('#td-apellido-'+participante_id).text() +'.',
                        type: 'error',
                        timeout: 2500,
                    }).show();
                    ocultar_copiar_form(total, completados);
                },
                url: api_url,
                success: function (respuesta) {
                    completados += 1;
                    new Noty({
                        text: 'Copiado con éxito',
                        type: 'success',
                        timeout: 1700,
                    }).show();
                    ocultar_copiar_form(total, completados);
                },
                type: 'POST'
            });
        })
    }

    var ocultar_copiar_form = function (total, completados) {
        if (completados >= total) {
            $('#copiar-form')[0].reset();
            $('.form-copiar').hide();
            $('.check-participante').prop('checked', false);
        }
    }

    GrupoDetail.init = function () {
        $('.editable').on('shown', function(e, editable) {
            $('.datepicker').datepicker({
                format: 'yyyy-mm-dd',
                autoclose: true,
                language: 'es'
            });
        }).editable({
            ajaxOptions: {
                contentType: 'application/json',
                dataType: 'json',
                type: "PATCH",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                }
            },
            params: function(params) {
                var obj = {};
                obj[params['name']] = params['value'];
                return JSON.stringify(obj);
            }
        });
        crear_grafico($("#grafico-asistencias"));
        $('.form-copiar').hide();
        $('#btn-select-all').click(function(){
            $('.check-participante').prop('checked',true);
        });
        $('#btn-select-none').click(function(){
            $('.check-participante:checkbox:checked').removeAttr('checked');
        });
        $('#btn-form-copiar').on('click', function () {
            $('.form-copiar').toggle();
        });
        $('#copiar-form').on('submit', function (e) {
            e.preventDefault();
            copiar_participantes();
        });
    }
}( window.GrupoDetail = window.GrupoDetail || {}, jQuery ));


(function( CalendarioCyD, $, undefined ) {
    var crear_cyd_calendario = function () {
        $('#cyd-calendario').fullCalendar({
            displayEventEnd: true,
            droppable: true, 
            drop: function (date, jsEvent, ui, resourceId) {
                update_event({
                    url: $(this).data('url'),
                    id: $(this).data('id'),
                    fecha: date.year()+'-'+(date.month()+1)+'-'+date.date(),
                    hora_inicio: date.hour()+':'+date.minute(),
                    hora_fin: ''
                });
            },
            editable: true,
            eventClick: function (calEvent, jsEvent, view) {
                var form = $('<form></form>');
                form.append('<div class="form-group"><label for="hora_inicio_m">Hora de inicio</label><input type="text" class="form-control" id="hora_inicio_m" value="'+calEvent.start.hour()+':'+calEvent.start.minute()+'"></div>');
                form.append('<div class="form-group"><label for="hora_fin_m">Hora de fin</label><input type="text" class="form-control" id="hora_fin_m" value="'+calEvent.end.hour()+':'+calEvent.end.minute()+'"></div>');
                bootbox.dialog({
                    message: form,
                    buttons: [
                    {
                        label: 'Cancelar',
                        className: 'btn-danger'
                    },
                    {
                        label: 'Guardar',
                        className: 'btn-success',
                        callback: function () {
                            update_event({
                                url: calEvent._url,
                                id: calEvent._id,
                                fecha: calEvent.start.year()+'-'+(calEvent.start.month()+1)+'-'+calEvent.start.date(),
                                hora_inicio: $('#hora_inicio_m').val(),
                                hora_fin: $('#hora_fin_m').val(),
                            });
                        }
                    }
                    ],
                });
            },
            eventDrop: function(event, delta, revertFunc, jsEvent, ui, view) {
                update_event({
                    url: event._url,
                    id: event._id,
                    fecha: event.start.year()+'-'+(event.start.month()+1)+'-'+event.start.date(),
                    hora_inicio: event.start.hour()+':'+event.start.minute(),
                    hora_fin: event.end.hour()+':'+event.end.minute(),
                });
            },
            eventDurationEditable: true,
            eventRender: function (event, element) {
                element.qtip({
                    content: {
                        title: event.curso,
                        text: event.description
                    },
                });
            },
            eventResize: function(event, delta, revertFunc, jsEvent, ui, view) {
                update_event({
                    url: event._url,
                    id: event._id,
                    fecha: event.start.year()+'-'+(event.start.month()+1)+'-'+event.start.date(),
                    hora_inicio: event.start.hour()+':'+event.start.minute(),
                    hora_fin: event.end.hour()+':'+event.end.minute(),
                });
            },
            eventSources: [
            {
                url: $('#cyd-calendario').data('url-cyd'),
                type: 'GET',
                cache: true,
                data: function () {
                    var params = {};
                    params['capacitador'] = $('#id_capacitador').val();
                    params['sede'] = $('#sede_form #id_sede').val();
                    return params;
                }
            }
            ],
            firstDay: 0,
            header: {
                left: 'prev,next today,month,agendaDay',
                center: '',
                right: 'title'
            },
            navLinks: false,
        });
    }

    function update_event(params) {
        $.ajax({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
            },
            url: params.url,
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                id: params.id,
                fecha: params.fecha,
                hora_inicio: params.hora_inicio,
                hora_fin: params.hora_fin
            },
            type: 'PATCH',
            success: function (calendario) {
                $('#drop-'+calendario.id).html('A'+calendario.cr_asistencia+' '+(calendario.fecha ? calendario.fecha : ''));
                $('#cyd-calendario').fullCalendar('refetchEvents');
                new Noty({
                    text: 'Guardado con éxito',
                    type: 'success',
                    timeout: 2000,
                    closeWith: ['click', 'button'],
                }).show();
            }
        })
    }

    function ini_events(ele) {
        ele.each(function () {
            var eventObject = {
                title: $.trim($(this).text())
            };

            $(this).data('eventObject', eventObject);

            $(this).draggable({
                zIndex: 1070,
                revert: true, 
                revertDuration: 0  
            });
        });
    }

    CalendarioCyD.init = function () {
        ini_events($('#asistencia_list div.external-event'));

        $('#sede_form #id_capacitador').on('change', function () {
            $.get($(this).data('url'), {capacitador: $(this).val()},
                function (respuesta) {
                    var options = '<option></option>';
                    $.each(respuesta, function (index, sede) {
                        options += '<option value="'+sede.id+'">'+sede.nombre+'</option>';
                    });
                    $('#sede_form #id_sede').html(options).trigger('change');
                });
        });

        $('#sede_form #id_sede').on('change', function () {
            $('#cyd-calendario').fullCalendar('refetchEvents');
        })

        $('#asistencia_form #id_sede').on('change', function () {
            $('#asistencia_form #id_grupo').html('');
            $('#asistencia_list').html('');
            if ($(this).val()) {
                $.get($(this).data('url'), {sede: $(this).val()},
                    function (respuesta) {
                        var options = '';
                        $.each(respuesta, function (index, grupo) {
                            options += '<option value="'+grupo.id+'">'+grupo.numero+' - '+grupo.curso+'</option>';
                        });
                        $('#asistencia_form #id_grupo').html(options).trigger('change');
                    });
            }
        });
        $('#asistencia_form #id_grupo').on('change', function () {
            $('#asistencia_list').html('');
            $.get($(this).data('url'), {grupo: $(this).val()},
                function (respuesta) {
                    var eventos = [];
                    $.each(respuesta, function (index, calendario) {
                        var event = $("<div />");
                        event.attr('id', 'drop-'+calendario.id);
                        event.attr('data-id', calendario.id);
                        event.attr('data-url', calendario.url);
                        event.addClass("external-event bg-aqua");
                        event.html('A'+calendario.cr_asistencia+' '+(calendario.fecha ? calendario.fecha : ''));
                        eventos.push(event);
                        ini_events(event);
                    });
                    $('#asistencia_list').html(eventos);
                });
        });
        if ($('#cyd-calendario').length) {
            crear_cyd_calendario();
        }
    }
}( window.CalendarioCyD = window.CalendarioCyD || {}, jQuery ));

(function( ParticipanteCrear, $, undefined ) {
    ParticipanteCrear.init = function () {
        /*
        Al cambiar la sede, genera el listado de grupos
        */
        $('#form_participante #id_sede').on('change', function () {
            listar_grupos_sede('#form_participante #id_sede', '#form_participante #id_grupo');
        });

        /*
        Al cambiar el grupo, genera el listado de participantes
        */
        $('#form_participante #id_grupo').on('change', function () {
            $('#tbody-listado').html('');
            $.get($(this).data('url'),
            {
                asignaciones__grupo: $(this).val(),
                fields: 'nombre,apellido,escuela'
            },
            function (respuesta) {
                var filas = [];
                $.each(respuesta, function (index, participante) {
                    var fila = $('<tr />');
                    fila.append('<td>'+participante.nombre+'</td>');
                    fila.append('<td>'+participante.apellido+'</td>');
                    fila.append('<td><a href="'+participante.escuela.url+'">'+participante.escuela.nombre+'<br>'+participante.escuela.codigo+'</a></td>');
                    filas.push(fila);
                });
                $('#tbody-listado').html(filas);
            });
        });

        /*
        Valida que el UDI ingresado sea real
        */
        $('#form_participante #id_udi').on('input', function () {
            $('#escuela_label').html('Escuela no encontrada');
            $('#btn-crear').prop('disabled', true);
            validar_udi_api({
                url: $(this).data('url'),
                udi: $(this).val(),
                callback: function (respuesta) {
                    if (respuesta.length>0) {
                        $('#escuela_label').html(respuesta[0].nombre);
                        $('#btn-crear').prop('disabled', false);
                    }
                    else{
                        $('#escuela_label').html('Escuela no encontrada');
                        $('#btn-crear').prop('disabled', true);
                    }
                }
            })
        });

        $('#form_participante').submit(function (e) {
            e.preventDefault();
            $.ajax({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
                },
                data: JSON.stringify($(this).serializeObject()),
                error: function (respuesta) {
                    new Noty({
                        text: 'Dato duplicado',
                        type: 'error',
                        timeout: 1500,
                    }).show();
                },
                success: function (respuesta) {
                    if(respuesta.status=="ok"){
                        $('#form_participante #id_grupo').trigger('change');
                        new Noty({
                            text: 'Creado con éxito',
                            type: 'success',
                            timeout: 1000,
                        }).show();
                        $('.form-reset').reset();
                    }
                    else{
                        bootbox.alert("Error desconocido.");
                    }
                },
                dataType: 'json',
                type: 'POST',
                url: $(this).attr('action')
            });
        });
    }
}( window.ParticipanteCrear = window.ParticipanteCrear || {}, jQuery ));

(function( ParticipanteImportar, $, undefined ) {
    var tabla_importar;
    var filas_borrar = [];
    var dpi_validator = function (dpi, callback) {
        if (dpi) {
            $.get(
                participante_api_list_url,
                {
                    dpi: dpi
                },
                function (respuesta) {
                    return respuesta.length > 0 ? callback(false) : callback(true);
                });
        }
    }

    var guardar_tabla = function () {
        var udi = $('#id_udi').val();
        var grupo = $('#id_grupo').val();
        var progress = 0;
        if (udi && grupo) {
            $.each(tabla_importar.getData(), function (index, fila) {
                if (fila[1] && fila[2] && fila[3] && fila[4]) {
                    try{
                        $.ajax({
                            beforeSend: function(xhr, settings) {
                                xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
                            },
                            data: JSON.stringify({
                                grupo: grupo,
                                udi: udi,
                                dpi: fila[0],
                                nombre: fila[1],
                                apellido: fila[2],
                                genero: fila[3],
                                rol: fila[4],
                                mail: fila[5],
                                tel_movil: fila[6],
                            }),
                            error: function (xhr, status, errorThrown) {
                                new Noty({
                                    text: 'Error al crear a ' + fila[1] + ' ' + fila[2],
                                    type: 'error',
                                    timeout: 3500,
                                }).show();
                                progress += 1;
                                notificar_fin(tabla_importar.countRows(), progress);
                            },
                            success: function (respuesta) {
                                if(respuesta.status=="ok"){
                                    progress += 1;
                                    filas_borrar.push(index + 1);
                                    notificar_fin(tabla_importar.countRows(), progress);
                                //tabla_importar.alter('remove_row', index);
                            }
                            else{
                                bootbox.alert("Error desconocido.");
                            }
                        },
                        contentType: "application/json; charset=utf-8",
                        dataType: 'json',
                        type: 'POST',
                        url: participante_add_ajax_url
                    });
                    }
                    catch(err){
                        console.log('asd');
                    }
                }
                else{
                    progress += 1;
                }
            });
        }
    }

    var notificar_fin = function(length_all, progress) {
        if (length_all == progress) {
            new Noty({
                text: 'Proceso terminado. Creados ' + filas_borrar.length + ' participantes.',
                type: 'success',
                timeout: 1000,
            }).show();
            filas_borrar.sort(function(a, b){return b-a});
            $('#btn-crear').prop('disabled', false);
            filas_borrar = [];
            $('#id_grupo').trigger('change');
            Pace.stop();
            tabla_importar.updateSettings({
                data : []
            });
        }
    }

    ParticipanteImportar.init = function () {
        $('#form_participante #id_sede').on('change', function () {
            listar_grupos_sede('#form_participante #id_sede', '#form_participante #id_grupo');
        });

        var container = document.getElementById('tabla_importar');

        tabla_importar = new Handsontable(container, {
            colHeaders: ["DPI", "Nombre", "Apellido", "Género", "Rol", "Correo electrónico", "Teléfono"],
            columns: [
            {data: 'dpi', validator: dpi_validator, allowInvalid: true},
            {data: 'nombre'},
            {data: 'apellido'},
            {
                type: 'handsontable',
                strict: true,
                handsontable: {
                    autoColumnSize: true,
                    data: ['M', 'F']
                }
            },
            {
                type: 'handsontable',
                strict: true,
                handsontable: {
                    autoColumnSize: true,
                    data: rol_list,
                    getValue: function () {
                        var selection = this.getSelected();
                        return this.getSourceDataAtRow(selection[0]).id;
                    }
                }
            },
            {data: 'email'},
            {data: 'tel_movil'},
            ],
            minSpareRows: 1,
            startRows: 1,
            rowHeaders: true,
        });

        /*
        Al cambiar el grupo, genera el listado de participantes
        */
        $('#form_participante #id_grupo').on('change', function () {
            $('#tbody-listado').html('');
            $.get($(this).data('url'),
            {
                asignaciones__grupo: $(this).val(),
                fields: 'nombre,apellido,escuela'
            },
            function (respuesta) {
                var filas = [];
                $.each(respuesta, function (index, participante) {
                    var fila = $('<tr />');
                    fila.append('<td>'+participante.nombre+'</td>');
                    fila.append('<td>'+participante.apellido+'</td>');
                    fila.append('<td><a href="'+participante.escuela.url+'">'+participante.escuela.nombre+'<br>'+participante.escuela.codigo+'</a></td>');
                    filas.push(fila);
                });
                $('#tbody-listado').html(filas);
            });
        });

        /*
        Valida que el UDI ingresado sea real
        */
        $('#form_participante #id_udi').on('input', function () {
            $('#escuela_label').html('Escuela no encontrada');
            $('#btn-crear').prop('disabled', true);
            validar_udi_api({
                url: $(this).data('url'),
                udi: $(this).val(),
                callback: function (respuesta) {
                    if (respuesta.length>0) {
                        $('#escuela_label').html(respuesta[0].nombre);
                        $('#btn-crear').prop('disabled', false);
                    }
                    else{
                        $('#escuela_label').html('Escuela no encontrada');
                        $('#btn-crear').prop('disabled', true);
                    }
                }
            })
        });

        $('#btn-crear').on('click', function () {
            $(this).prop('disabled', true);
            Pace.start();
            guardar_tabla();
        });

        $('#btn-clear').on('click', function () {
            tabla_importar.updateSettings({
                data : []
            });
        })
    }
}( window.ParticipanteImportar = window.ParticipanteImportar || {}, jQuery ));

(function( ParticipanteDetail, $, undefined ) {
    ParticipanteDetail.init = function () {
        $('.editable').editable({
            ajaxOptions: {
                contentType: 'application/json',
                dataType: 'json',
                type: "PATCH",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                }
            },
            error: function (response, newValue) {
                var respuesta = JSON.parse(response.responseText);
                var respuestaText = '';
                $.each(respuesta, function (index, item) {
                    respuestaText += item[0];
                });
                return respuestaText;
            },
            mode: 'inline',
            params: function(params) {
                var obj = {};
                obj[params['name']] = params['value'];
                return JSON.stringify(obj);
            },
        });
    }
}( window.ParticipanteDetail = window.ParticipanteDetail || {}, jQuery ));

(function( ParticipanteBuscar, $, undefined ) {
    var asignar_participante = function (participante_id) {
        var api_url = $('#participante-asignar-form').prop('action');
        var grupo_id = $('#participante-asignar-form #id_grupo').val();
        console.log(participante_id, grupo_id);
        if (grupo_id && participante_id) {
            $.ajax({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                },
                data: {
                    grupo: grupo_id,
                    participante: participante_id
                },
                dataType: 'json',
                error: function (respuesta) {
                    new Noty({
                        text: 'Error al realizar la asignación',
                        type: 'error',
                        timeout: 2500,
                    }).show();
                },
                url: api_url,
                success: function (respuesta) {
                    new Noty({
                        text: 'Asignado con éxito',
                        type: 'success',
                        timeout: 1700,
                    }).show();
                    $('#id_nombre').autocomplete('search');
                },
                type: 'POST'
            });
        }
    }

    ParticipanteBuscar.init = function () {
        $('#id_nombre').autocomplete({
            minLength: 4,
            selectFirst: false,
            search: function (event, ui) {
                $('#resultado-tbody').html('');
            },
            source: function (term, callback) {
                $.getJSON(
                    $('#participante-buscar-form').prop('action'),
                    {
                        search: term.term,
                        fields: 'id,nombre,apellido,escuela,url,asignaciones',
                        asignaciones__grupo__sede__capacitador: $('#participante-buscar-form #id_capacitador').val(),
                        asignaciones__grupo__sede: $('#participante-buscar-form #id_sede').val(),
                        asignaciones__grupo: $('#participante-buscar-form #id_grupo').val(),
                        escuela__codigo: $('#participante-buscar-form #id_udi').val(),
                        escuela__municipio__departamento: $('#participante-buscar-form #id_departamento').val(),
                        escuela__municipio: $('#participante-buscar-form #id_municipio').val()
                    },
                    callback);
            }
        }).data('ui-autocomplete')._renderItem = function (ul, item) {
            return $('<tr >')
                .data('item.autocomplete', item)
                .append(function () {
                    var td_participante = '';
                    td_participante += '<td><a href="'+item.url+'" class="btn btn-block">'+item.nombre+' '+item.apellido+'</a></td>';
                    td_participante += '<td>'+item.asignaciones.map(function (asignacion) {
                        return '<small class="badge bg-aqua">'+asignacion.grupo+'</small>';
                    }).join('<br />')+ '</td>';
                    td_participante += '<td><a href="'+item.escuela.url+'">'+item.escuela.nombre+'<br>'+item.escuela.codigo+'</a></td>';
                    if (permite_asignar) {
                        td_participante += '<td><button class="btn-asignar" data-pk="'+item.id+'">Asignar</button></td>';
                    }
                    return td_participante;
                })
                .appendTo($('#resultado-tbody'));
        };

        $('#participante-buscar-form #id_sede').on('change', function () {
            listar_grupos_sede('#participante-buscar-form #id_sede', '#participante-buscar-form #id_grupo', true);
        });
        $('#participante-buscar-form #id_grupo').on('change', function () {
            $('#id_nombre').autocomplete('search');
        });
        $('#participante-buscar-form #id_departamento').on('change', function () {
            listar_municipio_departamento('#participante-buscar-form #id_departamento', '#participante-buscar-form #id_municipio', true);
        });
        $('#participante-buscar-form #id_municipio').on('change', function () {
            $('#id_nombre').autocomplete('search');
        });

        $('#participante-asignar-form #id_sede').on('change', function () {
            listar_grupos_sede('#participante-asignar-form #id_sede', '#participante-asignar-form #id_grupo', true);
        });
        $(document).on("click", ".btn-asignar", function () {
            asignar_participante($(this).data('pk'));
        });
    }
}( window.ParticipanteBuscar = window.ParticipanteBuscar || {}, jQuery ));