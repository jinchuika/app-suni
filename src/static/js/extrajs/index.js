(function( HomePage, $, undefined ) {
	var crear_capacitacion_chart = function () {
		var ctx = document.getElementById("capacitacion_chart");
		$.post($(ctx).data('url'), function (data) {
			var capacitacion_chart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
					datasets: [{
						label: 'Escuelas',
						data: data.escuelas,
						backgroundColor: 'rgba(0, 166, 90, 0.8)',
						borderWidth: 1
					},
					{
						label: 'Escuelas Invitadas',
						data: data.invitadas,
						backgroundColor: 'rgba(239, 93, 14, 0.8)',
						borderWidth: 1
					},
					{
						label: 'Sedes',
						data: data.sedes,
						backgroundColor: 'rgba(0, 31, 63, 0.8)',
						borderWidth: 1
					},
					
				]
				},
				options: {
					hoverMode: 'index',
					scales: {
						xAxes: [{
                            stacked: true,
                        }],
						yAxes: [{
							stacked: true,
							ticks: {
								beginAtZero:true
							}
						}]
					},
					tooltips: {
						mode: 'label'
					},
				}
			});	
		});
	}

	var crear_equipamiento_chart = function () {
		var ctx = document.getElementById("equipamiento_chart");
		$.post($(ctx).data('url'), function (data) {
			var equipamiento_chart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
					datasets: [{
						label: 'Equipamientos',
						data: data.equipamiento,
						backgroundColor: 'rgba(0, 166, 90, 0.8)',
						borderWidth: 1
					},
					{
						label: 'Renovaciones',
						data: data.renovacion,
						backgroundColor: 'rgba(0, 31, 63, 0.8)',
						borderWidth: 1
					}]
				},
				options: {
					hoverMode: 'index',
					scales: {
						xAxes: [{
                            stacked: true,
                        }],
						yAxes: [{
							stacked: true,
							ticks: {
								beginAtZero:true
							}
						}]
					},
					tooltips: {
						mode: 'label'
					},
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
                        title: event.tip_title,
                        text: event.tip_text
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
	var crear_cyp_calendario = function () {
		$('#capacitacion-calendario').fullCalendar({
			firstDay: 0,
			header: {
				left: 'prev,next today',
				center: '',
				right: 'title'
			},

			navLinks: true,
			eventRender: function (event, element) {
                element.qtip({
                    content: {
                        title: event.tip_title,
                        text: event.tip_text
                    },
                });
            },
			eventSources: [
			{
				url: $('#capacitacion-calendario').data('url-capacitacion'),
				type: 'GET',
				cache: true
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
		if ($('#capacitacion_chart').length) {
			crear_capacitacion_chart();
		}
		if ($('#equipamiento_chart').length) {
			crear_equipamiento_chart();
		}
		if ($('#equipamiento-calendario').length) {
			crear_equipamiento_calendario();
		}
		if ($('#evento_dh-calendario').length) {
			crear_evento_dh_calendario();
		}
		if ($('#capacitacion-calendario').length) {
			crear_cyp_calendario();
		}
	}
}( window.HomePage = window.HomePage || {}, jQuery ));