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
    
    // Public
    EquipamientoList.init = function () {
    	$('#equipamiento-list-form').on('submit', function (e) {
    		e.preventDefault();
    		$.ajax({
	            type: 'post',
	            url: $(this).attr('action'),
	            dataType: 'json',
	            data: JSON.stringify($(this).serialize()),
	            success: function (respuesta) {
	                
	            }
	        });
    	});

    }   
}( window.EquipamientoList = window.EquipamientoList || {}, jQuery ));