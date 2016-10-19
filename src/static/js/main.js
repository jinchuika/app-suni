var GLOBALS = GLOBALS || (function(){
	var _args = {}; // private

	return {
		init : function(Args) {
			_args = Args;
		},
		get: function (key) {
			return _args[key];
		}
	};
}());
!function(a){a.fn.datepicker.dates.es={days:["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"],daysShort:["Dom","Lun","Mar","Mié","Jue","Vie","Sáb"],daysMin:["Do","Lu","Ma","Mi","Ju","Vi","Sa"],months:["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],monthsShort:["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],today:"Hoy",monthsTitle:"Meses",clear:"Borrar",weekStart:1,format:"dd/mm/yyyy"}}(jQuery);

$(document).ready(function () {
	$('.datepicker').datepicker({
		format: 'yyyy-mm-dd',
		autoclose: true,
		language: 'es'
	});



	$('.table-datatables').DataTable({
		"language":{
			"sProcessing":     "Procesando...",
			"sLengthMenu":     "Mostrar _MENU_ registros",
			"sZeroRecords":    "No se encontraron resultados",
			"sEmptyTable":     "Ningún dato disponible en esta tabla",
			"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
			"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
			"sInfoPostFix":    "",
			"sSearch":         "Buscar:",
			"sUrl":            "",
			"sInfoThousands":  ",",
			"sLoadingRecords": "Cargando...",
			"oPaginate": {
				"sFirst":    "Primero",
				"sLast":     "Último",
				"sNext":     "Siguiente",
				"sPrevious": "Anterior"
			},
			"oAria": {
				"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
				"sSortDescending": ": Activar para ordenar la columna de manera descendente"
			}
		}
	});


	$(".select2").select2({
		width : '100%'
	});
	$('#form_buscar_escuela').submit(function (e) {
		e.preventDefault();
		var queryParameters = {
			q: $('#id_nombre').val(),
			page_limit: $('#id_paginate').val(),
			forward: JSON.stringify({
				municipio: $('#id_municipio').val(),
				departamento: $('#id_departamento').val(),
				cooperante: $('#id_cooperante').val(),
				codigo: $('#codigo').val(),
				proyecto: $('#id_proyecto').val(),
				direccion: $('#id_direccion').val(),
			})
		}
		$.ajax({
			type: 'get',
			url: $('#id_nombre').data('ajax--url'),
			dataType: 'json',
			data: queryParameters,
			success: function (data) {
				$('#tbody-escuela').html('');
				$.each(data.results, function (index, escuela) {
					$('#tbody-escuela').append(get_fila_buscador_text(escuela.text));
				})
			}
		});
	});
	function get_fila_buscador_text(escuela) {
		var text = '<td><a href="'+escuela.url+'">'+escuela.nombre+'</a></td>';
		text += '<td>'+escuela.codigo+'</td>';
		text += '<td>'+escuela.direccion+'</td>';
		text += '<td>'+escuela.municipio+'</td>';
		text += '<td>'+escuela.departamento+'</td>';
		return '<tr>'+text+'</tr>';
	}
	$(".ajax-select2").select2({
		width : '100%',
		dropdownParent: $('#tabla_resultado'),
		ajax: {
			dataType: 'json',
			data: function (params) {
				var queryParameters = {
					q: params.term,
					forward: JSON.stringify({
						municipio: $('#id_municipio').val(),
						departamento: $('#id_departamento').val(),
						cooperante: $('#id_cooperante').val(),
						codigo: $('#codigo').val(),
						proyecto: $('#id_proyecto').val(),
					})
				}

				return queryParameters;
			},
			success: function (data) {
				console.log(data);
			}
		}

	});
});