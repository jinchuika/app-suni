
function buscar_escuela(params) {
	$.ajax({
		type: 'get',
		url: params.url,
		dataType: 'json',
		data: params.data,
		success: function (respuesta) {
			params.callback(respuesta);
		}
	});
}

function get_fila_buscador_text(escuela) {
	var text = '<td>'+escuela.codigo+'</td>';
	text += '<td><a href="'+escuela.url+'">'+escuela.nombre+'</a></td>';
	text += '<td>'+escuela.direccion+'</td>';
	text += '<td>'+escuela.municipio+'</td>';
	text += '<td>'+escuela.departamento+'</td>';
	text += '<td>'+escuela.nivel+'</td>';
	text += '<td>'+escuela.poblacion+'</td>';
	return '<tr>'+text+'</tr>';
}

$(document).ready(function () {
	/**
	 * BUSCADOR DE ESCUELAS
	 */

	$('#form_buscar_escuela').submit(function (e) {
		e.preventDefault();
		var queryParameters = {
			q: $('#id_codigo').val(),
			forward: JSON.stringify({
				municipio: $('#id_municipio').val(),
				departamento: $('#id_departamento').val(),
				cooperante: $('#id_cooperante').val(),
				nombre: $('#id_nombre').val(),
				proyecto: $('#id_proyecto').val(),
				direccion: $('#id_direccion').val(),
				nivel: $('#id_nivel').val(),
				poblacion_max: $('#id_poblacion_max').val(),
				poblacion_min: $('#id_poblacion_min').val(),
				solicitud: $('#id_solicitud').val(),
			})
		}
		buscar_escuela({
			url: $('#id_nombre').data('ajax--url'),
			data: queryParameters,
			callback: function (respuesta) {
				$('#tbody-escuela').html('');
				$('#encontradas').html(respuesta.results.length + " escuelas encontradas");
				$.each(respuesta.results, function (index, escuela) {
					$('#tbody-escuela').append(get_fila_buscador_text(escuela.text));
				});
			}
		});
	});

	/**
	 * PERFIL DE ESCUELAS
	 */

	$('#form-nueva-solicitud').hide();
	
})