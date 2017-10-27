var crear_organizacion_chart = function () {
	var ctx = document.getElementById("organizacion_chart");
	$.post($(ctx).data('url'), function (data) {
		var organizacion_chart = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
				datasets: [{
					label: 'Equipamientos',
					data: data.organizacion,
					backgroundColor: 'rgba(0, 166, 90, 0.8)',
					borderWidth: 1
				},
				{
					label: 'Renovaciones',
					data: data.renovacion,
					backgroundColor: 'rgba(243, 156, 18, 0.8)',
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

$(document).ready(function () {
	
});