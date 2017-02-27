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