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