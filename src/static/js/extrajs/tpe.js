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
    var armar_tabla = function (equipamiento_list) {
    	$('#equipamiento-table-body').html('');
    	var filas = ''
    	$.each(equipamiento_list, function (index, equipamiento) {
    		var fila = '<tr>';
    		fila += '<td><a href="'+equipamiento.entrega_url+'">' + equipamiento.entrega +'</a></td>';
    		fila += '<td><a href="'+equipamiento.escuela_url+'">' + equipamiento.escuela +'</a></td>';
    		fila += '<td>' + equipamiento.fecha +'</td>';
    		fila += '<td>' + equipamiento.renovacion +'</td>';
    		fila += '<td>' + equipamiento.khan +'</td>';
    		fila += '<td>' + equipamiento.cantidad_equipo +'</td>';
    		fila += '<td>' + equipamiento.tipo_red +'</td>';
    		fila += '<td>' + unir_campo(equipamiento.cooperante) + '</td>';
    		fila += '<td>' + unir_campo(equipamiento.proyecto) + '</td>';
    		fila += '</tr>';
    		filas += fila;
    	});
    	$('#equipamiento-table').DataTable().destroy();
    	$('#equipamiento-table-body').html(filas);
    	activar_datatable($('#equipamiento-table'));
    }

    var unir_campo = function (listado) {
    	return listado.map(function (item) {
    		return '<a href="'+item.url+'">'+item.nombre+'</a>';
		}).join("<br />")
    }

    // Public
    EquipamientoList.init = function () {
    	$('#equipamiento-list-form').on('submit', function (e) {
    		e.preventDefault();
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
}( window.EquipamientoList = window.EquipamientoList || {}, jQuery ));