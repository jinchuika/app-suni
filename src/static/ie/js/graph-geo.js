queue()
    .defer(d3.json, $('.origen-de-datos').data('url'))
    .await(makeGraphs);

function makeGraphs(error, projectsJson) {
	
	//Clean projectsJson data
	var donorschooseProjects = projectsJson;
	donorschooseProjects.forEach(function(d) {
		d["cantidad"] = +d["cantidad"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(donorschooseProjects);

	//Define Dimensions
	var nivelDim = ndx.dimension(function(d) { return d["nivel"]; });
	var areaDim = ndx.dimension(function(d) { return d["area"]; });
	var sectorDim = ndx.dimension(function(d) { return d["sector"]; });
	var departamentoDim = ndx.dimension(function(d) { return d["departamento"]; });
	var totalDim  = ndx.dimension(function(d) { return d["cantidad"]; });


	//Calculate metrics
	var numProjectsByResourceType = nivelDim.group().reduceSum(function(d) {
		return d["cantidad"];
	});
	var numProjectsByPovertyLevel = areaDim.group().reduceSum(function(d) {
		return d["cantidad"];
	});
	var sectorLevel = sectorDim.group().reduceSum(function(d) {
		return d["cantidad"];
	});
	var escuelasDepartamento = departamentoDim.group().reduceSum(function(d) {
		return d["cantidad"];
	});

	var all = ndx.groupAll();
	var totalDonations = ndx.groupAll().reduceSum(function(d) {return d["cantidad"];});

	var max_departamento = escuelasDepartamento.top(1)[0].value;


    //Charts
	var nivelChart = dc.barChart("#resource-type-row-chart");
	var departamentoChart = dc.rowChart("#us-chart");
	var areaChart = dc.pieChart("#poverty-level-row-chart");
	var sectorChart = dc.pieChart("#sector-chart");
	var numeroLaboratoriosND = dc.numberDisplay("#number-projects-nd");
	var escuelasChart = dc.numberDisplay("#total-donations-nd");
	var visCount = dc.dataCount(".dc-data-count");

	numeroLaboratoriosND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	escuelasChart
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDonations)
		.formatNumber(d3.format(".3s"));

	nivelChart
        .width(550)
        .height(250)
        .gap(1)
  		.margins({top: 0, right: 0, bottom: 95, left: 30})
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .brushOn(false)
        .elasticY(true)
        .dimension(nivelDim)
        .group(numProjectsByResourceType)
        .colors(d3.scale.ordinal().range(['#078965']))
        .xAxis().ticks(4);

    nivelChart.on("postRender", function(c) {rotateBarChartLabels();} );

        function rotateBarChartLabels() {
        	d3.selectAll('#resource-type-row-chart > svg > g > g.axis.x text')
        	.style("text-anchor", "end" )
        	.attr("transform", function(d) { return "rotate(-50, -4, 9) "; });
        }

    departamentoChart
        .width(550)
        .height(650)
        .elasticX(true)
        .dimension(departamentoDim)
        .group(escuelasDepartamento)
        .xAxis().ticks(4);

	areaChart
		.width(300)
		.height(250)
        .dimension(areaDim)
        .colors(d3.scale.ordinal().range(['#46B1C9', '#E4572E']))
        .group(numProjectsByPovertyLevel);

    sectorChart
		.width(300)
		.height(250)
        .dimension(sectorDim)
        .colors(d3.scale.ordinal().range(['#E8803E', '#166088', '#1BCF76', '#129490']))
        .group(sectorLevel);

    visCount
    	.dimension(ndx)
    	.group(totalDonations);

    dc.renderAll();

};