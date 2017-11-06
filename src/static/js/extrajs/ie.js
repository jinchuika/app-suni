(function( ValidacionInforme, $, undefined ) {
    var tabla = $('#validacion-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#validacion-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#validacion-list-form').serializeObject();
            }
        },
        columns: [
        {
            data: "id",
            render: function (data, type, full) {
                return '<a class="btn btn-block" href="' + full.url + '">' + data + '</a>';
            }
        },
        {
            data: "escuela",
            render: function (data) {
                return '<a href="' + data.url + '">' + data.nombre + '<br>(' + data.codigo + ')</a>';
            }
        },
        {data: "departamento"},
        {data: "municipio"},
        {data: "fecha_inicio", "className": "nowrap", type: "date"},
        {data: "fecha_fin", "className": "nowrap", type: "date"},
        {
            data: "completada",
            render: function (data) {
                return data == true ? 'Sí' : 'No';
            }
        },
        {data: "porcentaje_requisitos" },
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    ValidacionInforme.init = function () {
        $('#spinner').hide();
        $('#validacion-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    } 
}( window.ValidacionInforme = window.ValidacionInforme || {}, jQuery ));


(function( LaboratorioInforme, $, undefined ) {
    var tabla = $('#laboratorio-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#laboratorio-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#laboratorio-list-form').serializeObject();
            }
        },
        columns: [
        {
            data: "id",
            render: function (data, type, full) {
                return '<a class="btn btn-block" href="' + full.url + '">' + data + '</a>';
            }
        },
        {
            data: "escuela",
            render: function (data) {
                return '<a href="' + data.url + '">' + data.nombre + '<br>(' + data.codigo + ')</a>';
            }
        },
        {data: "departamento"},
        {data: "municipio"},
        {data: "fecha", "className": "nowrap", type: "date"},
        {data: "cantidad_computadoras" },
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    LaboratorioInforme.init = function () {
        $('#spinner').hide();
        $('#laboratorio-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    } 
}( window.LaboratorioInforme = window.LaboratorioInforme || {}, jQuery ));
