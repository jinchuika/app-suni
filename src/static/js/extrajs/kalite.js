(function( VisitaDetail, $, undefined ) {
	var get_promedios = function () {
		$('.promedio-evaluacion').each(function (index, promedio) {
			get_promedio_individual(promedio);
		});
	}

	var get_promedio_visita = function () {
		var visita = $('#promedio-visita');
		$.ajax({
			url: $(visita).data('url'),
			data: {fields: 'promedio'},
			dataType: 'json',
			success: function (resultado) {
				$(visita).html(resultado.promedio + "%");
				$('#progressbar-visita').css('width', parseInt(resultado.promedio)+'%');
			},
		});
	}

	var get_promedio_individual = function (promedio) {
		var evaluacion_id = $(promedio).data('id');
		var progressbar = $('#progressbar-'+evaluacion_id);
		$.ajax({
			url: $(promedio).data('url'),
			data: {fields: 'promedio'},
			dataType: 'json',
			success: function (resultado) {
				$(promedio).html(resultado.promedio);
				$('#promedio-evaluacion-graph-'+evaluacion_id).html(resultado.promedio + "%");
				$(progressbar).css('width', parseInt(resultado.promedio)+'%');
			},
		});
	}

    // Public
    VisitaDetail.init = function () {
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
            mode: 'inline',
            params: function(params) {
                var obj = {};
                obj[params['name']] = params['value'];
                return JSON.stringify(obj);
            },
            success: function (resultado, nuevo) {
            	if (resultado.evaluacion) {
            		get_promedio_individual($('#evaluacion-'+resultado.evaluacion));
            		get_promedio_visita();
            	}
            }
        });
        get_promedios();
    }
}( window.VisitaDetail = window.VisitaDetail || {}, jQuery ));