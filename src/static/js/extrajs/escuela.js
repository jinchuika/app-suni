(function( BuscadorEscuela, $, undefined ) {
    //Private Property
    var get_form = function () {
        $('#tbody-escuela').html('');
        return {
            q: $('#id_codigo').val(),
            forward: JSON.stringify({
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
                equipamiento: $('#id_equipamiento').val(),
                equipamiento_id: $('#id_equipamiento_id').val(),
                departamento_tpe: $('#id_departamento_tpe').val(),
                cooperante_tpe: $('#id_cooperante_tpe').val(),
            })
        }
    };

    var buscar_escuela = function (params) {
        $.ajax({
            type: 'get',
            url: params.url,
            dataType: 'json',
            data: params.data,
            success: function (respuesta) {
                params.callback(respuesta);
            }
        });
    };

    var get_fila_text = function (escuela) {
        var text = '<td>'+escuela.codigo+'</td>';
        text += '<td><a href="'+escuela.url+'">'+escuela.nombre+'</a></td>';
        text += '<td>'+escuela.direccion+'</td>';
        text += '<td>'+escuela.municipio+'</td>';
        text += '<td>'+escuela.departamento+'</td>';
        text += '<td>'+escuela.nivel+'</td>';
        text += '<td>'+escuela.poblacion+'</td>';
        return '<tr>'+text+'</tr>';
    };

    // Public
    BuscadorEscuela.init = function () {
        $('#form_buscar_escuela').submit(function (e) {
            e.preventDefault();
            $('#encontradas').html("Buscando...");
            buscar_escuela({
                url: $('#id_nombre').data('ajax--url'),
                data: get_form(),
                callback: function (respuesta) {
                    $('#encontradas').html(respuesta.results.length + " escuelas encontradas");
                    $.each(respuesta.results, function (index, escuela) {
                        $('#tbody-escuela').append(get_fila_text(escuela.text));
                    });
                }
            });
        });
    }   
}( window.BuscadorEscuela = window.BuscadorEscuela || {}, jQuery ));

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

    var crear_monitoreo = function (url, comentario) {
        var data = {
            "comentario": comentario
        }
        $.post(url, JSON.stringify(data)).then(function (respuesta) {
            var fecha = new Date(respuesta.fecha);
            var td_fecha = $('<td></td>').text(fecha.getFullYear() + "-" + (fecha.getMonth()+1) + "-" + fecha.getDate());
            var td_usuario = $('<td></td>').text(respuesta.usuario);
            var td = $('<td></td>').text(respuesta.comentario);
            var tr = $('<tr></tr>').append(td).append(td_usuario). append(td_fecha);
            $('#body-monitoreo-' + respuesta.equipamiento_id).append(tr);
        });
    }

    // Public
    PerfilEscuela.init = function () {
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
                    console.log(result + id_validacion);
                }
            });
        });

        $('.monitoreo-form').submit(function (e) {
            e.preventDefault();
            var url = $(this).prop('action');
            bootbox.prompt({
                title: "Nuevo registro de monitoreo",
                inputType: 'textarea',
                callback: function (comentario) {
                    if (comentario) {
                        crear_monitoreo(url, comentario);
                    }
                }
            });
        })
    }   
}( window.PerfilEscuela = window.PerfilEscuela || {}, jQuery ));

(function( EscuelaBuscar, $, undefined ) {
    var tabla = $('#escuela-table').DataTable({
        "paging":   false,
    });
    var filtro_list = [];
    var armar_tabla = function (escuela_list) {
        $.each(escuela_list, function (index, escuela) {
            tabla.row.add([
                escuela.codigo,
                '<a href="'+escuela.escuela_url+'">' + escuela.nombre + '</a>',
                escuela.direccion,
                escuela.departamento,
                escuela.municipio,
                escuela.sector,
                escuela.nivel,
                escuela.poblacion,
                (escuela.equipada ? 'Sí' : 'No')
                ]).draw(false);
        });
        $('#escuela-table tbody tr').each(function(){
            $(this).find('td:eq(0)').attr('nowrap', 'nowrap');
        });
        $('#lista-filtros').append('<li>'+filtro_list.join('</li><li>')+'</li>')
        $('#filtros-collapse').show();
    }

    var buscar_escuela = function (form) {
        $.ajax({
            type: 'post',
            url: $(form).attr('action'),
            dataType: 'json',
            data: $(form).serialize(),
            success: function (respuesta) {
                armar_tabla(respuesta);
            }
        });
    }

    // Public
    EscuelaBuscar.init = function () {
        $('#escuela-list-form').submit(function (e) {
            e.preventDefault();
            filtro_list = [];
            tabla.clear().draw();
            $('#lista-filtros').empty();

            $("#escuela-list-form :input").not(':submit,:button,:hidden').each(function() {
                if($(this).val() != ""){
                    filtro_list.push($("label[for='"+$(this).attr('id')+"']").text());
                }
            });
            
            if (filtro_list.length > 0) {
                $('#filtros-collapse').hide();
                buscar_escuela($(this));
            }
            else{
                $('#lista-filtros').append('<li>Seleccione al menos un filtro</li>');
                $('#filtros-collapse').show();
            }
        });

    }   
}( window.EscuelaBuscar = window.EscuelaBuscar || {}, jQuery ));

$(document).ready(function () {
    /**
     * PERFIL DE ESCUELAS
     */

    $('#form-nueva-solicitud').hide();
    $('#form-nuevo-equipamiento').hide();
    $('#form-nueva-validacion').hide();
    
})