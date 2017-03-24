(function( DetalleGarantia, $, undefined ) {

    // Public
    DetalleGarantia.init = function () {
    	$('#form-nuevo-ticket').hide();
    	$('.form-nuevo-registro').hide();
    	$('#button-nuevo-ticket').on('click', function () {
    		$('#form-nuevo-ticket').toggle();
    	});

    }   
}( window.DetalleGarantia = window.DetalleGarantia || {}, jQuery ));

(function( EquipamientoList, $, undefined ) {
    var tabla = $('#equipamiento-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#equipamiento-list-form').serializeObject();
            }
        },
        columns: [
        { "data": "entrega"},
        { "data": "escuela"},
        { "data": "fecha", "className": "nowrap"  },
        { "data": "renovacion" },
        { "data": "khan" },
        { "data": "cantidad" },
        { "data": "tipo_red" },
        { "data": "cooperante", 'render': '[, <br>].cooperante' },
        { "data": "proyecto", 'render': '[, <br>].proyecto' },
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
         $('#spinner').hide();
    });

    // Public
    EquipamientoList.init = function () {
        $('#spinner').hide();
        $('#equipamiento-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    } 
}( window.EquipamientoList = window.EquipamientoList || {}, jQuery ));

(function( MonitoreoList, $, undefined ) {
    var tabla = $('#monitoreo-table').DataTable({
        "paging":   false,
        rowsGroup: [
        3, 2, 0, 1
        ],
    });
    var armar_tabla = function (monitoreo_list) {
        $.each(monitoreo_list, function (index, equipamiento) {
            tabla.row.add([
                equipamiento.departamento,
                equipamiento.municipio,
                equipamiento.escuela,
                equipamiento.entrega,
                equipamiento.fecha,
                equipamiento.comentario
                ]).draw(false);
        });
    }

    // Public
    MonitoreoList.init = function () {
        $('#monitoreo-list-form').submit(function (e) {
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
}( window.MonitoreoList = window.MonitoreoList || {}, jQuery ));