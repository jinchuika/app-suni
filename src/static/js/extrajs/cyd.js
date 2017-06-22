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


(function( GrupoDetail, $, undefined ) {
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

        $('#id_sede').on('change', function () {
            $('#id_grupo').html('');
            $('#asistencia_list').html('');
            if ($('#id_sede').val()) {
                $.get($(this).data('url'), {sede: $(this).val()},
                    function (respuesta) {
                        var options = '';
                        $.each(respuesta, function (index, grupo) {
                            options += '<option value="'+grupo.id+'">'+grupo.numero+' - '+grupo.curso+'</option>';
                        });
                        $('#id_grupo').html(options).trigger('change');
                    });
            }
        });
        $('#id_grupo').on('change', function () {
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