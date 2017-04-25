(function( HomePage, $, undefined ) {
	var equipamiento_chart = function () {
		var barChartCanvas = $("#barChart").get(0).getContext("2d");
		var barChart = new Chart(barChartCanvas);
		var barChartData = areaChartData;
		barChartData.datasets[1].fillColor = "#00a65a";
		barChartData.datasets[1].strokeColor = "#00a65a";
		barChartData.datasets[1].pointColor = "#00a65a";
		var barChartOptions = {
			scaleBeginAtZero: true,
			scaleShowGridLines: true,
			scaleGridLineColor: "rgba(0,0,0,.05)",
			scaleGridLineWidth: 1,
			scaleShowHorizontalLines: true,
			scaleShowVerticalLines: true,
			barShowStroke: true,
			barStrokeWidth: 2,
			barValueSpacing: 5,
			barDatasetSpacing: 1,
			legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
			responsive: true,
			maintainAspectRatio: true
		};

		barChartOptions.datasetFill = false;
		barChart.Bar(barChartData, barChartOptions);
	}
	HomePage.init = function () {
		if ($('#equipamiento_chart').length) {
			console.log("wii");
			equipamiento_chart();
		}
	}
}( window.HomePage = window.HomePage || {}, jQuery ));