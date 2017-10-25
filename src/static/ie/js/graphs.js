queue()
    .defer(d3.json, "/ie/api/laboratorio/")
    .await(makeGraphs);

function makeGraphs(error, projectsJson) {
	
	//Clean projectsJson data
	var donorschooseProjects = projectsJson;
	var dateFormat = d3.time.format("%Y-%m-%d");
	donorschooseProjects.forEach(function(d) {
		d["fecha"] = dateFormat.parse(d["fecha"]);
		d["fecha"].setDate(1);
		d["computadoras"] = +d["computadoras"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(donorschooseProjects);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["fecha"]; });
	var orgDim = ndx.dimension(function(d) { return d["organizacion"]; });
	var povertyLevelDim = ndx.dimension(function(d) { return d["area"]; });
	var municipioDim = ndx.dimension(function(d) { return d["municipio"]; });
	var departamentoDim = ndx.dimension(function(d) { return d["departamento"]; });
	var totalDonationsDim  = ndx.dimension(function(d) { return d["computadoras"]; });


	//Calculate metrics
	var numProjectsByDate = dateDim.group(); 
	var numProjectsByResourceType = orgDim.group();
	var numProjectsByPovertyLevel = povertyLevelDim.group();
	var totalDonationsByState = municipioDim.group().reduceSum(function(d) {
		return d["computadoras"];
	});
	var totalComputadorasDepartamento = departamentoDim.group().reduceSum(function(d) {
		return d["computadoras"];
	});

	var all = ndx.groupAll();
	var totalDonations = ndx.groupAll().reduceSum(function(d) {return d["computadoras"];});

	var max_state = totalDonationsByState.top(1)[0].value;
	var max_departamento = totalComputadorasDepartamento.top(1)[0].value;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["fecha"];
	var maxDate = dateDim.top(1)[0]["fecha"];

    //Charts
	var timeChart = dc.barChart("#time-chart");
	var orgChart = dc.rowChart("#resource-type-row-chart");
	var departamentoChart = dc.rowChart("#us-chart");
	var areaChart = dc.pieChart("#poverty-level-row-chart");
	var numeroLaboratoriosND = dc.numberDisplay("#number-projects-nd");
	var numeroComputadorasND = dc.numberDisplay("#total-donations-nd");

	numeroLaboratoriosND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	numeroComputadorasND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDonations)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(260)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numProjectsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Año")
		.yAxis().ticks(4);

	orgChart
        .width(600)
        .height(250)
        .dimension(orgDim)
        .group(numProjectsByResourceType)
        .xAxis().ticks(4);

    departamentoChart
        .width(600)
        .height(550)
        .dimension(departamentoDim)
        .group(totalComputadorasDepartamento)
        .xAxis().ticks(4);

	areaChart
		.width(200)
		.height(200)
        .dimension(povertyLevelDim)
        .colors(d3.scale.ordinal().range(['#BCB382', '#09814A']))
        .group(numProjectsByPovertyLevel);
    dc.renderAll();

};