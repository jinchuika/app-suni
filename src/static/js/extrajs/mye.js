(function( InformeMye, $, undefined ) {
    var get_extra_campos = function () {
        var lista = [];
        $.each($("input[name='campos']:checked"), function(){            
            lista.push($(this).val());
        });
        return lista;
    }
    //Private Property
    var get_form = function () {
        $('#tbody-escuela').html('');
        return JSON.stringify({
            municipio: $('#id_municipio').val(),
            departamento_mye: $('#id_departamento_mye').val(),
            cooperante_mye: $('#id_cooperante_mye').val(),
            nombre: $('#id_nombre').val(),
            proyecto: $('#id_proyecto').val(),
            direccion: $('#id_direccion').val(),
            nivel: $('#id_nivel').val(),
            sector: $('#id_sector').val(),
            poblacion_max: $('#id_poblacion_max').val(),
            poblacion_min: $('#id_poblacion_min').val(),
            solicitud: $('#id_solicitud').val(),
            solicitud_id: $('#id_solicitud_id').val(),
            validada: $('#id_validada').val(),
            validacion_id: $('#id_validacion_id').val(),
            equipamiento: $('#id_equipamiento').val(),
            equipamiento_id: $('#id_equipamiento_id').val(),
            departamento_tpe: $('#id_departamento_tpe').val(),
            cooperante_tpe: $('#id_cooperante_tpe').val(),
            extras: get_extra_campos()
        });
    };

    var buscar_escuela = function (params) {
        $.ajax({
            type: 'post',
            url: params.url,
            dataType: 'json',
            data: params.data,
            success: function (respuesta) {
                params.callback(respuesta);
            }
        });
    };

    var get_fila_text = function (escuela) {
        var text = '<td nowrap>'+escuela.codigo+'</td>';
        text += '<td><a href="'+escuela.url+'">'+escuela.nombre+'</a></td>';
        text += '<td>'+escuela.municipio+'</td>';
        text += '<td>'+escuela.departamento+'</td>';
        text += '<td>'+escuela.nivel+'</td>';
        text += '<td>'+escuela.poblacion+'</td>';
        $.each(escuela.extras, function (field, value) {
            text += '<td>'+value+'</td>';
        });
        return '<tr>'+text+'</tr>';
    };

    // Public
    InformeMye.init = function () {
        $('#form_buscar_escuela').submit(function (e) {
            e.preventDefault();
            $('#encontradas').html("Buscando...");
            buscar_escuela({
                url: $('#id_nombre').data('ajax--url'),
                data: get_form(),
                callback: function (respuesta) {
                    $('#encontradas').html(respuesta.length + " escuelas encontradas");
                    $.each(respuesta, function (index, escuela) {
                        $('#tbody-escuela').append(get_fila_text(escuela));
                    });
                }
            });
        });
    }   
}( window.InformeMye = window.InformeMye || {}, jQuery ));


(function( SolicitudList, $, undefined ) {
    var tabla = $('#solicitud-table').DataTable({
        "paging":   false,
    });
    
    var armar_tabla = function (solicitud_list) {
        $.each(solicitud_list, function (index, solicitud) {
            tabla.row.add([
                solicitud.departamento,
                solicitud.municipio,
                '<a href="'+solicitud.escuela_url+'">' + solicitud.escuela + '</a>',
                solicitud.alumnos,
                solicitud.maestros,
                join_requisito(solicitud.requisitos),
                ]).draw(false);
        });
    }

    var join_requisito = function (requisito_list) {
        return requisito_list.map(function (item) {
            return (item.cumple ? '✔ ' : '✖ ') + item.req;
        }).join("<br />")
    }

    // Public
    SolicitudList.init = function () {
        $('#solicitud-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $.ajax({
                type: 'post',
                url: $(this).attr('action'),
                dataType: 'json',
                data: $(this).serialize(),
                success: function (respuesta) {
                    armar_tabla(respuesta);
                }
            });
        });

    }   
}( window.SolicitudList = window.SolicitudList || {}, jQuery ));


(function( ValidacionList, $, undefined ) {
    var tabla = $('#validacion-table').DataTable({
        "paging":   false,
    });
    var armar_tabla = function (validacion_list) {
        $.each(validacion_list, function (index, validacion) {
            tabla.row.add([
                validacion.departamento,
                validacion.municipio,
                '<a href="'+validacion.escuela_url+'">' + validacion.escuela + '</a>',
                '<a href="'+validacion.validacion_url+'">' + validacion.estado + '</a>',
                join_requisito(validacion.requisitos),
                validacion.historial.map(function (item) {
                    return '- ' + item.comentario;
                }).join('<br />')
                ]).draw(false);
        });
    }

    var join_requisito = function (requisito_list) {
        return requisito_list.map(function (item) {
            return (item.cumple ? '✔ ' : '✖ ') + item.req;
        }).join("<br />")
    }

    // Public
    ValidacionList.init = function () {
        $('#validacion-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $.ajax({
                type: 'post',
                url: $(this).attr('action'),
                dataType: 'json',
                data: $(this).serialize(),
                success: function (respuesta) {
                    armar_tabla(respuesta);
                }
            });
        });

    }   
}( window.ValidacionList = window.ValidacionList || {}, jQuery ));