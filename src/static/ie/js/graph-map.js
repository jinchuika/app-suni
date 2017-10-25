queue()
.defer(d3.json, "/ie/api/escuela/")
.await(makeGraphs);

var vista_calor = false;

function cambiar_vista() {
    vista_calor = !vista_calor;
    makeGraphs().drawMap();    
}

function makeGraphs(error, recordsJson) {

    /* Carga de datos */
    var records = recordsJson;

    records.forEach(function(d) {
        d["lng"] = +d["lng"];
        d["lat"] = +d["lat"];
    });

    /* Filtros cruzados */
    var ndx = crossfilter(records);

    /* Dimensiones a utilizar */
    var departamentoDim = ndx.dimension(function(d) { return d["departamento"]; });
    var municipiodDim = ndx.dimension(function(d) { return d["municipio"]; });
    var allDim = ndx.dimension(function(d) {return d;});

    /* Grupos de datos */
    var phoneBrandGroup = departamentoDim.group();
    var municipioGroup = municipiodDim.group();
    var all = ndx.groupAll();

    /* Gráficos */
    var numberRecordsND = dc.numberDisplay("#number-records-nd");
    var departamentoChart = dc.rowChart("#phone-brand-row-chart");
    var municipioChart = dc.selectMenu("#municipio-row-chart");

    numberRecordsND
    .formatNumber(d3.format("d"))
    .valueAccessor(function(d){return d; })
    .group(all)
    .formatNumber(d3.format("5s"));

    departamentoChart
    .width(400)
    .height(450)
    .dimension(departamentoDim)
    .group(phoneBrandGroup)
    .ordering(function(d) { return -d.value })
    .elasticX(true)
    .xAxis().ticks(4);

    municipioChart
    .width(200)
    .height(510)
    .dimension(municipiodDim)
    .group(municipioGroup)
    .promptText('')
    .ordering(function(d) { return -d.value });

    municipioChart.on('postRender', function () {
        $('.dc-select-menu').select2();
        $('.dc-select-menu').on('change', function () {
            if ($(this).val() && $(this).val() != "") {
                municipioChart.replaceFilter([$(this).val()]);
            } else {
                municipioChart.filterAll();
            }
            dc.events.trigger(function () {
                dc.redrawAll();
            });
        });
    });

    var map = L.map('map');

    var circleStyle = function(point) {
        return {
            fillColor: colors[point.type]
        };
    };

    var drawMap = function(calor){
        map.setView([15.719, -90.35], 8);
        mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
        L.tileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; ' + mapLink + ' Contributors',
                maxZoom: 15,
            }).addTo(map);

        /* HeatMap */
        var geoData = [];

        /* Cluster de marcadores */
        var markerCluster = L.markerClusterGroup({ chunkedLoading: true });

        _.each(allDim.top(Infinity), function (d) {
            geoData.push([d["lat"], d["lng"], 1]);
            markerCluster.addLayer(L.marker(L.latLng(d["lat"], d["lng"])));
        });

        if (calor) {
            var heat = L.heatLayer(geoData, {
                radius: 10,
                blur: 20, 
                maxZoom: 1,
            }).addTo(map);
        }
        else{
            map.addLayer(markerCluster);
        }

    };

    /* Crear mapa */
    drawMap(vista_calor);

    /* Actualizar el mapa con los filtros */
    dcCharts = [departamentoChart, municipioChart];
    _.each(dcCharts, function (dcChart) {
        dcChart.on("filtered", function (chart, filter) {
            map.eachLayer(function (layer) {
                map.removeLayer(layer)
            }); 
            drawMap(vista_calor);
        });
    });

    $('#btn-layer').click(function () {
        vista_calor = !vista_calor;
        map.eachLayer(function (layer) {
            map.removeLayer(layer)
        }); 
        drawMap(vista_calor);
    })

    dc.renderAll();
};
