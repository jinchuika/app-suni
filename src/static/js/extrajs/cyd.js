(function( BuscadorSede, $, undefined ) {
	BuscadorSede.init = function () {
		var options = {
			valueNames: [ 'sede', 'capacitador']
		};
		var userList = new List('buscador', options);
		
		$('#id_capacitador').change(function () {
			var tr = $('.tr-sede');
			if ($(this).val() == '') {
				$(tr).show();
				return false;
			}
			for (var i = 0; i < tr.length; i++) {
				if($(tr[i]).data('capacitador-id') == $(this).val()) {
					$(tr[i]).show();
				}
				else{
					$(tr[i]).hide();
				}
			}
		})

	}
}( window.BuscadorSede = window.BuscadorSede || {}, jQuery ));

(function( GrupoDetail, $, undefined ) {
	GrupoDetail.init = function () {
		$('.editable').on('shown', function(e, editable) {
			$('.datepicker').datepicker({
				format: 'yyyy-mm-dd',
				autoclose: true,
				language: 'es'
			});
		}).editable({
			ajaxOptions: {
				contentType: 'application/json',
				dataType: 'json',
				type: "PATCH",
				beforeSend: function(xhr, settings) {
					xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
				}
			},
			params: function(params) { 
				var obj = {};
				obj[params['name']] = params['value'];
				return JSON.stringify(obj);
			}
		});
	}
}( window.GrupoDetail = window.GrupoDetail || {}, jQuery ));