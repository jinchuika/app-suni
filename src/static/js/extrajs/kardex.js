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
        $('.btn-entrada').on('click', function () {
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
        $('.btn-salida').on('click', function () {
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
          })
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
