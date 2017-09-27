(function( EquipoList, $, undefined ) {
    var tabla_equipo = $('#tabla-equipo').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf']
    });

    var tabla_entrada = $('#tabla-entrada').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        columns: [
            {
                data: 'entrada',
                render: function ( data, type, full, meta ) {
                    return '<a href="' + full.entrada_url + '">' + data + '</a>';
                }
            },
            {
                data: 'fecha',
                className: 'nowrap'
            },
            {data: 'cantidad'},
        ]
    });

    var tabla_salida = $('#tabla-salida').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        columns: [
            {
                data: 'salida',
                render: function ( data, type, full, meta ) {
                    return '<a href="' + full.salida_url + '">' + data + '</a>';
                }
            },
            {
                data: 'fecha',
                className: 'nowrap'
            },
            {data: 'cantidad'},
        ]
    });

    EquipoList.init = function () {
        $('#form-equipo').hide();
        $('.box-informe').hide();
        $('#btn-equipo-add').click(function () {
            $('#form-equipo').toggle();
        });

        // Generar listados de entradas
        $('#tabla-equipo').on('click', '.btn-entrada', function () {
            $('.box-informe').hide();
            tabla_entrada.clear().draw();
            $.ajax({
                url: $(this).data('url'),
                data: {
                    equipo: $(this).data('pk'),
                    fields: 'entrada,fecha,cantidad,entrada_url'
                },
                success: function (respuesta) {
                    $('#box-entrada').show();
                    tabla_entrada.rows.add(respuesta).draw();
                }
            });
        });

        // Generar listados de salidas
        $('#tabla-equipo').on('click', '.btn-salida', function () {
            $('.box-informe').hide();
            tabla_salida.clear().draw();
            $.ajax({
                url: $(this).data('url'),
                data: {
                    equipo: $(this).data('pk'),
                    fields: 'salida,fecha,cantidad,salida_url'
                },
                success: function (respuesta) {
                    $('#box-salida').show();
                    tabla_salida.rows.add(respuesta).draw();
                }
            });
        });
    }
}( window.EquipoList = window.EquipoList || {}, jQuery ));


(function( ProveedorList, $, undefined ) {
    ProveedorList.init = function () {
        $('#proveedor-tabla').DataTable();
        $('.btn-proveedor').click(function () {
            $.ajax({
                url: $('#proveedor-tabla').data('url-entrada'),
                data: {
                    proveedor: $(this).data('id')
                }
            })
        })
    }
}( window.ProveedorList = window.ProveedorList || {}, jQuery ));


(function( EntradaCreate, $, undefined ) {
    EntradaCreate.init = function () {
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
                        tr += '<td nowrap>'+entrada.fecha+'</td>';
                        tr += '<td>'+entrada.proveedor+'</td>';
                        tr += '<td>'+(entrada.factura ? entrada.factura : '')+'</td>';
                        tr += '<td>Q. '+entrada.precio_total+'</td>';
                        $('#tbody-entradas').append('<tr>'+tr+'</tr>');
                    })
                }
            });
        });
    }
}( window.EntradaCreate = window.EntradaCreate || {}, jQuery ));


(function( SalidaCreate, $, undefined ) {
    SalidaCreate.init = function () {
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
            })
        });

        $('#filter-form').submit(function (e) {
            e.preventDefault();
            $('#tbody-salidas').empty();
            $.ajax({
                url: $(this).prop('action'),
                data: $(this).serializeObject(),
                success: function (respuesta) {
                    var tr = '';
                    $.each(respuesta, function (index, salida) {
                        tr = '<td><a href="'+salida.url+'" class="btn btn-block">'+salida.id+'</a></td>';
                        tr += '<td nowrap>'+salida.fecha+'</td>';
                        tr += '<td>'+salida.tecnico+'</td>';
                        $('#tbody-salidas').append('<tr>'+tr+'</tr>');
                    })
                }
            });
        });
    }
}( window.SalidaCreate = window.SalidaCreate || {}, jQuery ));


(function( KardexInforme, $, undefined ) {
    var tabla;

    // Public
    KardexInforme.init = function () {
        tabla = $('#inventario-table').DataTable({
            dom: 'lfrtipB',
            buttons: ['excel','pdf'],
            processing: true,
            ajax: {
                url: $('#kardex-informe-form').prop('action'),
                type: "get",
                deferRender: true,
                dataSrc: '',
                data: function () {
                    return $('#kardex-informe-form').serializeObject();
                }
            },
            columns: [
            { "data": "nombre"},
            { "data": "cantidad_entrada"},
            { "data": "cantidad_salida"},
            { "data": "inventario_entrada"},
            { "data": "inventario_salida"},
            {
                data: 'existencia',
                render: function ( data, type, full, meta ) {
                    return full.inventario_entrada - full.inventario_salida;
                }
            },            
            { "data": "existencia" },
            ]
        }).on('xhr.dt', function (e, settings, json, xhr) {
            $('#spinner').hide();
        });

        $('#spinner').hide();
        $('#kardex-informe-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
        
    } 
}( window.KardexInforme = window.KardexInforme || {}, jQuery ));

(function( SalidaDetail, $, undefined ) {
    SalidaDetail.init = function () {
        $('#id_equipo').on('change', function () {
            var id_equipo = $(this).val();
            $('#btn-agregar').prop('disabled', true);
            if (id_equipo) {
                $.ajax({
                    url: $('#detalle-form').data('url-validacion'),
                    data: {
                        id: id_equipo,
                        field: 'existencia'
                    },
                    dataType: 'json',
                    success: function (respuesta) {
                        $('#id_cantidad').prop('max', respuesta[0].existencia);
                        $('#btn-agregar').prop('disabled', false);
                    }
                })
            }
        });
    }
}( window.SalidaDetail = window.SalidaDetail || {}, jQuery ));