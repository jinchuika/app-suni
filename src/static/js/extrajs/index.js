(function( HomePage, $, undefined ) {
	var crear_equipamiento_chart = function () {
		var ctx = document.getElementById("equipamiento_chart");
		$.post($(ctx).data('url'), function (data) {
			var equipamiento_chart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
					datasets: [{
						label: 'Equipamientos',
						data: data,
						backgroundColor: 'rgba(0, 166, 90, 0.8)',
						borderWidth: 1
					}]
				},
				options: {
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero:true
							}
						}]
					}
				}
			});	
		});
	}

	var crear_equipamiento_calendario = function () {
		$('#equipamiento-calendario').fullCalendar({
			header: {
				left: 'prev,next today',
				center: '',
				right: 'title'
			},

			navLinks: true,
			eventRender: function (event, element) {
                element.qtip({
                    content: {
                        title: event.municipio,
                        text: event.direccion
                    },
                });
            },
			eventSources: [
			{
				url: $('#equipamiento-calendario').data('url-validacion'),
				type: 'GET',
				color: 'orange',
				cache: true,
			},
			{
				url: $('#equipamiento-calendario').data('url-equipamiento'),
				type: 'GET',
				color: 'green',
				cache: true,
			}
			]
		});
	}

	var crear_evento_dh_calendario = function () {
		$('#evento_dh-calendario').fullCalendar({
			header: {
				left: 'prev,next today,month,listYear',
				center: '',
				right: 'title'
			},

			navLinks: true, 
			eventSources: [
			{
				url: $('#evento_dh-calendario').data('url-evento_dh'),
				type: 'GET',
				cache: true,
			}
			]
		});
	}

	HomePage.init = function () {
		if ($('#equipamiento_chart').length) {
			crear_equipamiento_chart();
		}
		if ($('#equipamiento-calendario').length) {
			crear_equipamiento_calendario();
		}
		if ($('#evento_dh-calendario').length) {
			crear_evento_dh_calendario();
		}
	}
}( window.HomePage = window.HomePage || {}, jQuery ));