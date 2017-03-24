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
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#solicitud-list-form').serializeObject();
            }
        },
        columns: [
        { "data": "departamento", "className": "nowrap" },
        { "data": "municipio", "className": "nowrap" },
        { "data": "escuela" },
        { "data": "alumnos" },
        { "data": "maestros" },
        { "data": "fecha", "className": "nowrap" },
        { "data": "requisitos" }
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#solicitud-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
         $('#spinner').hide();
    });

    // Public
    SolicitudList.init = function () {
        $('#spinner').hide();
        $('#solicitud-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    }   
}( window.SolicitudList = window.SolicitudList || {}, jQuery ));


(function( ValidacionList, $, undefined ) {
    var tabla = $('#validacion-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#validacion-list-form').serializeObject();
            }
        },
        columns: [
        { data: "departamento", className: "nowrap" },
        { data: "municipio", className: "nowrap" },
        { data: "escuela" },
        {
            data: "estado",
            render: function (data) {
                return '<a href="'+data.url+'">'+data.estado+'</a>';
            }
        },
        { data: "requisitos",},
        { data: "comentarios", render: "[<br />].comentario" }
        ]
    }).on('xhr.dt', function () {
         $('#spinner').hide();
    });;

    // Public
    ValidacionList.init = function () {
        $('#spinner').hide();
        $('#validacion-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $('#spinner').show();
            tabla.ajax.reload();
        });

    }   
}( window.ValidacionList = window.ValidacionList || {}, jQuery ));