(function( BuscadorEscuela, $, undefined ) {
    //Private Property
    var get_form = function () {
		$('#tbody-escuela').html('');
		return {
			q: $('#id_codigo').val(),
			forward: JSON.stringify({
				municipio: $('#id_municipio').val(),
				departamento: $('#id_departamento').val(),
				cooperante: $('#id_cooperante').val(),
				nombre: $('#id_nombre').val(),
				proyecto: $('#id_proyecto').val(),
				direccion: $('#id_direccion').val(),
				nivel: $('#id_nivel').val(),
				sector: $('#id_sector').val(),
				poblacion_max: $('#id_poblacion_max').val(),
				poblacion_min: $('#id_poblacion_min').val(),
				solicitud: $('#id_solicitud').val(),
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


$(document).ready(function () {
	/**
	 * PERFIL DE ESCUELAS
	 */

	$('#form-nueva-solicitud').hide();
	$('#form-nuevo-equipamiento').hide();
	
})