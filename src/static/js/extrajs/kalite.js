(function( VisitaDetail, $, undefined ) {
    var get_promedios = function () {

        $('.promedio-evaluacion').each(function (index, promedio) {
            get_promedio_individual(promedio);
        });
    }

    var get_promedio_escuela = function () {
        /*
                Actualiza el widget que muestra el promedio de la visita.
                Se llama cada vez que se actualiza una evaluación mediante x-editable.
         */
        var visita = $('#promedio-escuela');     // el widget que muestra el promedio de la visita
        $.ajax({
            url: $(visita).data('url'),         // el widget tiene la URL
            data: {fields: 'promedio_escuela'},         // únicamente pide le promedio para minimizar el tráfico
            dataType: 'json',
            success: function (resultado) {
                // Actualiza la cantidad en el encabezado del widget
                $(visita).html(resultado.promedio_escuela + "%");
                // Actualiza la barra de progreso del wdiget
                $('#progressbar-visita').css('width', parseInt(resultado.promedio_escuela)+'%');
            },
        });
    }

    var get_promedio_visita= function () {
        /*
                Actualiza el widget que muestra el promedio de la visita.
                Se llama cada vez que se actualiza una evaluación mediante x-editable.
         */
        var visita = $('#promedio-visita');     // el widget que muestra el promedio de la visita
        $.ajax({
            url: $(visita).data('url'),         // el widget tiene la URL
            data: {fields: 'promedio'},         // únicamente pide le promedio para minimizar el tráfico
            dataType: 'json',
            success: function (resultado) {
                // Actualiza la cantidad en el encabezado del widget
                $(visita).html(resultado.promedio + "%");
                // Actualiza la barra de progreso del wdiget
                $('#progressbar-visita').css('width', parseInt(resultado.promedio)+'%');
            },
        });
    }


    var get_promedio_individual = function (evaluacion) {
        /*
                Obtiene el promedio de cada evaluación (mediante Ajax) y actualiza
                el encabezado del box y el widget correspondiente.
                Es llamada por `get_promedios` al iniciar la página.
         */
        var evaluacion_id = $(evaluacion).data('id');
        var progressbar = $('#progressbar-'+evaluacion_id); // la barra del widget correspondiente a la evaluación
        $.ajax({
            url: $(evaluacion).data('url'), // la url de la evaluación
            data: {fields: 'promedio'},     // únicamente pide le promedio para minimizar el tráfico
            dataType: 'json',
            success: function (resultado) {
                $(evaluacion).html(resultado.promedio);
                // Actualiza el texto en el widget de la evaluación
                $('#promedio-evaluacion-graph-'+evaluacion_id).html(resultado.promedio + "%");
                // Actualiza la barra de progreso en base al porcentaje
                $(progressbar).css('width', parseInt(resultado.promedio)+'%');
            },
        });
    }

    var crear_grado = function (grado_form) {
        $.ajax({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            url: $(grado_form).prop('action'),
            data: $(grado_form).serializeObject(),
            dataType: 'json',
            success: function (resultado) {
                // hace el render del nuevo grado con editable=1
                render_grado(resultado);
                $(grado_form).hide();
            },
            type: "post"
        });
    }

    var get_grados = function (grado_accordion) {
        $.ajax({
            url: $(grado_accordion).data('url'),
            data: {'visita': $(grado_accordion).data('visita')},
            dataType: 'json',
            success: function (resultado) {
                $.each(resultado, function (index, grado) {
                    render_grado(grado, 1);
                });
            },
            type: "get"
        });
    }

    /*
    * Crea la tabla con detalle de los datos del grado
    */
    var tabla_grado = function (grado) {
        var tabla = '<table class="table" id="tabla-grado-'+grado.id+'">';
        // Cantidad de ejercicios esperados
        tabla += '<tr><th>Esperado</th><td>'+grado.minimo_esperado+'</td></tr>';
        tabla += '<tr><th>Alcanzados</th><td>'+grado.alcanzados+'</td></tr>';
        tabla += '<tr><th>Por nivelar</th><td>'+grado.nivelar+'</td></tr>';
        tabla += '<tr><th>Total estudiantes</th><td>'+grado.total_estudiantes+'</td></tr>';
        tabla += '<tr><th>Total ejercicios</th><td>'+grado.total_ejercicios+'</td></tr>';
        tabla += '<tr><th>Promedio</th><td>'+grado.promedio_ejercicios+'</td></tr>';
        tabla += '</table>';
        VisitaDetail.listado_grados[grado.id] = {
            'grado': grado.grado + ' ' + grado.seccion,
            'alcanzados': grado.alcanzados,
            'nivelar': grado.nivelar,
            'promedio': grado.promedio_ejercicios};
        VisitaDetail.grado_chart_update();
        return tabla;
    }

    var render_grado = function (data) {
        var panel = $('<div class="panel box box-danger"></div>');
        var panel_content = '<div class="box-header">';
        // panel header
        panel_content += '<h4 class="box-title">';
        panel_content += '<a data-toggle="collapse" data-parent="#accordion" href="#grado-'+data.id+'" aria-expanded="false" class="collapsed">';
        panel_content += data.grado+' '+data.seccion+'</a></h4></div>';

        // panel body
        panel_content += '<div id="grado-'+data.id+'" class="panel-collapse collapse" aria-expanded="false" style="height: 0px;">'
        panel_content += '<div class="box-body table-responsive">';

        //tabla resumen
        panel_content += '<table class="table">';

        panel_content += tabla_grado(data);
        panel_content += '</div></div>';

        $(panel).append(panel_content);
        $('#grado-accordion').append(panel);
        activar_edicion_grado();
    }

    var activar_edicion = function (callback) {
        if (VisitaDetail.puede_editar) {
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
                    if (callback) {
                        callback(resultado);
                    }
                }
            });
        }
    }

    var activar_edicion_grado = function () {
        // para activar la edición después de agregar un grado
        // o un registro de Ejercicios por Estudiantes
        activar_edicion(function (resultado, nuevo) {
            // valida que se haya editado un grado
            if (resultado.visita) {
                $('#tabla-grado-'+resultado.id).remove();
                $('#grado-'+resultado.id).append(tabla_grado(resultado));
            }
            else if (resultado.estudiantes) {
                // si lo que editó fue un registro de ejercicios por estudiantes
                // solicita el nuevo resumen del grado
                $.ajax({
                    url: resultado.grado_url,
                    data: {
                        fields: 'id,grado,seccion,alcanzados,nivelar,total_ejercicios,total_estudiantes,promedio_ejercicios'
                    },
                    success: function (resultado) {
                        $('#tabla-grado-'+resultado.id).remove();
                        $('#grado-'+resultado.id).append(tabla_grado(resultado));
                    }
                });
            }
        });
    }

    VisitaDetail.nuevo_ejgr = function (grado_id) {
        bootbox.prompt('Cantidad de ejercicios', function (ejercicios) {
            if (ejercicios) {
                $.ajax({
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                    },
                    url: $('#grado-accordion').data('url-ejgr'),
                    data: {
                        grado: grado_id,
                        ejercicios: ejercicios,
                        estudiantes: 0
                    },
                    type: 'post',
                    success: function (ejgr) {
                        var tabla = '<tr><td>';
                        tabla += '<a href="#" class="editable btn btn-block" data-url="'+ejgr.url+'" data-pk="'+ejgr.id+'" data-name="estudiantes" data-type="text">';
                        tabla += ejgr.estudiantes + '</a></td><td>';
                        tabla += '<a href="#" class="editable btn btn-block" data-url="'+ejgr.url+'" data-pk="'+ejgr.id+'" data-name="ejercicios" data-type="text">';
                        tabla += ejgr.ejercicios + '</a></td><td></tr>';
                        $('#tabla-ejercicios-'+ejgr.grado).append(tabla);
                        //activa que se pueda editar
                        activar_edicion_grado();
                    }
                })
            }
        });
    }

    VisitaDetail.listado_grados = {};

    VisitaDetail.grado_chart_data = {
        labels: [],
        datasets: [{
            label: 'Alcanzados',
            backgroundColor: '#00a65a',
            borderWidth: 1,
            yAxisID: "y-axis-1",
            data: []
        }, {
            label: 'Nivelar',
            backgroundColor: '#0073b7',
            borderWidth: 1,
            yAxisID: "y-axis-1",
            data: []
        }, {
            label: 'Promedio',
            borderColor: '#0073b7',
            borderWidth: 1,
            yAxisID: "y-axis-2",
            type: 'line',
            data: []
        }]
    }

    VisitaDetail.grado_chart_update = function () {
        var labels = [];
        var alcanzados = [];
        var nivelar = [];
        var promedio = [];
        $.each(VisitaDetail.listado_grados, function (index, grado) {
            labels.push(grado['grado']);
            alcanzados.push(grado['alcanzados']);
            nivelar.push(grado['nivelar']);
            promedio.push(grado['promedio']);
        });
        
        VisitaDetail.grado_chart_data.labels = labels;
        VisitaDetail.grado_chart_data.datasets[0].data = alcanzados;
        VisitaDetail.grado_chart_data.datasets[1].data = nivelar;
        VisitaDetail.grado_chart_data.datasets[2].data = promedio;
        VisitaDetail.grado_chart.update();
    }

    // Public
    VisitaDetail.init = function (puede_editar) {
        VisitaDetail.puede_editar = puede_editar;
        activar_edicion(function (resultado) {
            if (resultado.evaluacion) {
                get_promedio_individual($('#evaluacion-'+resultado.evaluacion));
                get_promedio_visita();
                get_promedio_escuela();
            }
        });
        $('#form-grado').hide();
        $('#form-grado').submit(function (e) {
            e.preventDefault();
            crear_grado(this);
        });
        get_promedios();
        get_grados($('#grado-accordion'));
        $('.btn-ejgr').on('click', function () {
            nuevo_ejgr($(this).data('grado-id'));
        });
        VisitaDetail.grado_chart = new Chart(document.getElementById("grafico-grados"), {
            type: 'bar',
            data: VisitaDetail.grado_chart_data,
            options: {
                tooltips: {
                    mode: 'label'
                },
                responsive: true,
                hoverMode: 'index',
                title:{
                    display: true,
                    text:'Rendimiento de los grados'
                },
                scales: {
                    yAxes: [{
                        type: "linear",
                        display: true,
                        position: "left",
                        id: "y-axis-1",
                    }, {
                        type: "linear",
                        display: true,
                        position: "right",
                        id: "y-axis-2",
                        gridLines: {
                            drawOnChartArea: false,
                        },
                    }],
                }

            }
        });
    }
}( window.VisitaDetail = window.VisitaDetail || {}, jQuery ));


(function( CalendarioKalite, $, undefined ) {
    var crear_kalite_calendario = function () {
        $('#kalite-calendario').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,listMonth'
            },
            height: 650,
            navLinks: true,
            eventRender: function (event, element) {
                element.qtip({
                    content: {
                        title: event.tip_title,
                        text: event.tip_text
                    },
                });
            },
            eventSources: [{
                url: $('#kalite-calendario').data('url-calendario'),
                type: 'GET',
                color: 'orange',
                cache: true,
                data: function () {
                    return $('#calendario-form').serializeObject();
                }
            }]
        });
    }

    // Public
    CalendarioKalite.init = function () {
        crear_kalite_calendario();
        $('#id_capacitador').on('change', function(){
            $('#kalite-calendario').fullCalendar( 'refetchEvents' );
        })
    } 
}( window.CalendarioKalite = window.CalendarioKalite || {}, jQuery ));

(function( VisitaEscuelaInforme, $, undefined ) {
    VisitaEscuelaInforme.tabla = $('#visita-escuela-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#visita-list-form').prop('action'),
            deferRender: true,
            cache: false,
            dataSrc: '',
            data: function () {
                return $('#visita-list-form').serializeObject();
            }
        },
        columns: [
        {
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + data.url + '">' + data.nombre + '</a>';
            }
        },
        {
            data: 'escuela.codigo',
            "class": 'nowrap'
        },
        {data: "municipio"},
        {data: "departamento"},
        {data: "capacitador"},
        {data: "numero"},
        {data: "promedio"},
        {data: "alcance"},
        {data: "fecha", "class": 'nowrap'},
        {data: "poblacion"},
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#visita-escuela-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
         $('#spinner').hide();
    });

    // Public
    VisitaEscuelaInforme.init = function () {
        $('#spinner').hide();
        $('#visita-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            VisitaEscuelaInforme.tabla.clear().draw();
            VisitaEscuelaInforme.tabla.ajax.reload();
        });
    }
}( window.VisitaEscuelaInforme = window.VisitaEscuelaInforme || {}, jQuery ));

(function( VisitaInforme, $, undefined ) {
    VisitaInforme.tabla = $('#visita-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#visita-list-form').prop('action'),
            deferRender: true,
            cache: false,
            dataSrc: '',
            data: function () {
                return $('#visita-list-form').serializeObject();
            }
        },
        columns: [
        {
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + data.url + '">' + data.nombre + '</a>';
            }
        },
        {
            data: 'escuela.codigo',
            class: 'nowrap'
        },
        {data: "municipio"},
        {data: "departamento"},
        {data: "capacitador"},
        {data: "numero"},
        {data: "promedio"},
        {data: "alcance"},
        {data: "fecha", class: 'nowrap'},
        {data: "poblacion"},
        {data: "estudiantes"},
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#visita-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
         $('#spinner').hide();
    });

    // Public
    VisitaInforme.init = function () {
        $('#spinner').hide();
        $('#visita-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            VisitaInforme.tabla.clear().draw();
            VisitaInforme.tabla.ajax.reload();
        });
    }   
}( window.VisitaInforme = window.VisitaInforme || {}, jQuery ));


(function( VisitaDashboard, $, undefined ) {
    // Public
    VisitaDashboard.init = function () {
        queue()
            .defer(d3.json, $('.origen-de-datos').data('url'))
            .await(makeGraphs);

        function makeGraphs(error, visitaJson) {
            
            //Clean visitaJson data
            var visitaData = visitaJson;
            var formatoFecha = d3.time.format("%Y-%m-%d");
            visitaData.forEach(function(d) {
                d["fecha"] = formatoFecha.parse(d["fecha"]);
                d["promedio"] = +d["promedio"];
            });

            // Instancia de filtros cruzados
            var ndx = crossfilter(visitaData);

            // Dimensiones a utilizar
            var fechaDim = ndx.dimension(function(d) { return d["fecha"]; });
            var capacitadorDim = ndx.dimension(function(d) { return d["capacitador"]; });
            var alcanceDim = ndx.dimension(function(d) { return d["alcance"]; });
            var departamentoDim = ndx.dimension(function(d) { return d["departamento"]; });
            var numeroDim = ndx.dimension(function(d) { return d["numero"]; });
            var promedioDim  = ndx.dimension(function(d) { return d["promedio"]; });


            //Calculate metrics
            function reducePromedioAdd (p, v) {
                ++p.count;
                p.total += v.promedio;
                return p;
            }
            function reducePromedioRemove(p, v) {
                --p.count;
                p.total -= v.promedio;
                return p;
            }
            function reducePromedioInit() {
                return {count: 0, total: 0};
            }
            var numProjectsByDate = fechaDim.group(); 
            var orgGroup = capacitadorDim.group();
            var numeroGroup = numeroDim.group();
            var alcanceGroup = alcanceDim.group();
            var departamentoGroup = departamentoDim.group().reduce(reducePromedioAdd, reducePromedioRemove, reducePromedioInit);

            var all = ndx.groupAll();
            var promedioGroup = ndx.groupAll().reduce(reducePromedioAdd, reducePromedioRemove, reducePromedioInit);

            var max_departamento = departamentoGroup.top(1)[0].value;

            //Define values (to be used in charts)
            var minDate = fechaDim.bottom(1)[0]["fecha"];
            var maxDate = fechaDim.top(1)[0]["fecha"];

            //Charts
            var fechaChart = dc.barChart("#time-chart");
            var capacitadorChart = dc.barChart("#resource-type-row-chart");
            var departamentoChart = dc.rowChart("#us-chart");
            var alcanceChart = dc.pieChart("#alcance-pie-chart");
            var cantidadVisitas = dc.numberDisplay("#cantidad-visitas");
            var promedioGeneral = dc.numberDisplay("#rendimiento-promedio");
            var numeroChart = dc.barChart("#numero-visita");

            cantidadVisitas
                .formatNumber(d3.format("d"))
                .valueAccessor(function(d){return d; })
                .group(all);

            promedioGeneral
                .formatNumber(d3.format("d"))
                .valueAccessor(function(p) { return p.count > 0 ? p.total / p.count : 0; })
                .group(promedioGroup)
                .formatNumber(d3.format(".3s"));

            numeroChart
                .width(300)
                .height(250)
                .dimension(numeroDim)
                .group(numeroGroup)
                .x(d3.scale.ordinal())
                .xUnits(dc.units.ordinal)
                .elasticY(true);

            fechaChart
                .width(600)
                .height(200)
                .margins({top: 10, right: 50, bottom: 30, left: 50})
                .dimension(fechaDim)
                .group(numProjectsByDate)
                .transitionDuration(500)
                .x(d3.time.scale().domain([minDate, maxDate]))
                .brushOn(true)
                .xAxis().ticks(d3.time.month);

            capacitadorChart
                .x(d3.scale.ordinal())
                .xUnits(dc.units.ordinal)
                .width(300)
                .height(250)
                .dimension(capacitadorDim)
                .group(orgGroup)
                .elasticY(true)
                .xAxis().ticks(4);

            departamentoChart
                .valueAccessor(function(p) { return p.value.count > 0 ? p.value.total / p.value.count : 0; })
                .width(600)
                .height(350)
                .dimension(departamentoDim)
                .group(departamentoGroup)
                .xAxis().ticks(4);

            alcanceChart
                .width(350)
                .height(350)
                .dimension(alcanceDim)
                .colors(d3.scale.ordinal().range(['#dd4b39', '#f39c12', '#00a65a']))
                .group(alcanceGroup);
            dc.renderAll();

        };
    }   
}( window.VisitaDashboard = window.VisitaDashboard || {}, jQuery ));