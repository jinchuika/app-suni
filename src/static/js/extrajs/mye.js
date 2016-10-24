$(document).ready(function () {
	$('#id_codigo').keyup(function () {
		var codigo = $(this).val();
		if(codigo.length > 12){
			buscar_escuela({
				url: $(this).data('url'),
				data: {q: codigo},
				callback: function (respuesta) {
					if(respuesta.results.length > 0){
						$('#id_escuela').val(respuesta.results[0].id);
					}
				}
			});
		}
	});
});