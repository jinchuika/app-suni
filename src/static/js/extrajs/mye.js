(function( InformeMye, $, undefined ) {
    var get_extra_campos = function () {
        var lista = [];
        $.each($("input[name='campos']:checked"), function(){
            lista.push($(this).val());
        });
        return lista;
    }
    //Private Property
    var get_form = function () {
        $('#tbody-escuela').html('');
        return JSON.stringify({
            municipio: $('#id_municipio').val(),
            departamento_mye: $('#id_departamento_mye').val(),
            cooperante_mye: $('#id_cooperante_mye').val(),
            nombre: $('#id_nombre').val(),
            proyecto: $('#id_proyecto').val(),
            direccion: $('#id_direccion').val(),
            nivel: $('#id_nivel').val(),
            sector: $('#id_sector').val(),
            poblacion_max: $('#id_poblacion_max').val(),
            poblacion_min: $('#id_poblacion_min').val(),
            solicitud: $('#id_solicitud').val(),
            solicitud_id: $('#id_solicitud_id').val(),
            validada: $('#id_validada').val(),
            validacion_id: $('#id_validacion_id').val(),
            equipamiento: $('#id_equipamiento').val(),
            equipamiento_id: $('#id_equipamiento_id').val(),
            departamento_tpe: $('#id_departamento_tpe').val(),
            cooperante_tpe: $('#id_cooperante_tpe').val(),
            extras: get_extra_campos()
        });
    };

    var buscar_escuela = function (params) {
        $.ajax({
            type: 'post',
            url: params.url,
            dataType: 'json',
            data: params.data,
            success: function (respuesta) {
                params.callback(respuesta);
            }
        });
    };

    var get_fila_text = function (escuela) {
        var text = '<td nowrap>'+escuela.codigo+'</td>';
        text += '<td><a href="'+escuela.url+'">'+escuela.nombre+'</a></td>';
        text += '<td>'+escuela.municipio+'</td>';
        text += '<td>'+escuela.departamento+'</td>';
        text += '<td>'+escuela.nivel+'</td>';
        text += '<td>'+escuela.poblacion+'</td>';
        $.each(escuela.extras, function (field, value) {
            text += '<td>'+value+'</td>';
        });
        return '<tr>'+text+'</tr>';
    };

    // Public
    InformeMye.init = function () {
        $('#form_buscar_escuela').submit(function (e) {
            e.preventDefault();
            $('#encontradas').html("Buscando...");
            buscar_escuela({
                url: $('#id_nombre').data('ajax--url'),
                data: get_form(),
                callback: function (respuesta) {
                    $('#encontradas').html(respuesta.length + " escuelas encontradas");
                    $.each(respuesta, function (index, escuela) {
                        $('#tbody-escuela').append(get_fila_text(escuela));
                    });
                }
            });
        });
    }
}( window.InformeMye = window.InformeMye || {}, jQuery ));


(function( SolicitudList, $, undefined ) {
    var tabla = $('#solicitud-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#solicitud-list-form').prop('action'),
            deferRender: true,
            cache: false,
            dataSrc: '',
            data: function () {
                return $('#solicitud-list-form').serializeObject();
            }
        },
        columns: [
        {"data": "departamento", "className": "nowrap"},
        {"data": "municipio", "className": "nowrap"},
        {
            "data": "escuela",
            render: function (data) {
                return '<a href="'+data.url+'">'+data.nombre+'<br>('+data.codigo+')</a>';
            }
        },
        { "data": "alumnos" },
        { "data": "maestros" },
        { "data": "fecha", "className": "nowrap" },
        {
            "data": "requisitos",
            render: function (data) {
                return parseInt(data) + "%";
            }
        }
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#solicitud-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
        $('#spinner').hide();
    });

    // Public
    SolicitudList.init = function () {
        $('#spinner').hide();
        $('#solicitud-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
    }
}( window.SolicitudList = window.SolicitudList || {}, jQuery ));


(function( ValidacionList, $, undefined ) {
    var tabla = $('#validacion-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#validacion-list-form').prop('action'),
            deferRender: true,
            dataSrc: '',
            cache: false,
            data: function () {
                return $('#validacion-list-form').serializeObject();
            }
        },
        columns: [
        {data: "departamento", className: "nowrap" },
        {data: "municipio", className: "nowrap" },
        {
            "data": "escuela",
            render: function (data) {
                return '<a href="'+data.url+'">'+data.nombre+'<br>('+data.codigo+')</a>';
            }
        },
        {data: "estado"},
        {data: "fecha", className: "nowrap"},
        {data: "fecha_equipamiento", className: "nowrap"},
        {
            "data": "requisitos",
            render: function (data) {
                return parseInt(data) + "%";
            }
        },
        {
            "data": "comentarios",
            render: function (data) {
                return $.map(data, function (comentario, index) {
                    return '- ' + comentario.comentario;
                }).join('<br>');
            }
        }
        ]
    }).on('xhr.dt', function () {
       $('#spinner').hide();
   });;

    // Public
    ValidacionList.init = function () {
        $('#spinner').hide();
        $('#validacion-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $('#spinner').show();
            tabla.ajax.reload();
        });

    }
}( window.ValidacionList = window.ValidacionList || {}, jQuery ));


(function( CooperanteList, $, undefined ) {
    var tabla = $('#cooperante-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#cooperante-list-form').prop('action'),
            deferRender: true,
            dataSrc: '',
            cache: false,
            data: function () {
                return $('#cooperante-list-form').serializeObject();
            }
        },
        columns: [
        {
            "data": "nombre",
            render: function (data, type, full) {
                return '<a href="'+full.url+'">'+full.nombre+'</a>';
            }
        },
        {data: "cantidad_equipamientos", className: "nowrap" },
        {data: "cantidad_computadoras", className: "nowrap" }
        ]
    }).on('xhr.dt', function () {
       $('#spinner').hide();
   });;

    // Public
    CooperanteList.init = function () {
        $('#spinner').hide();
        $('#cooperante-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $('#spinner').show();
            tabla.ajax.reload();
        });

    }
}( window.CooperanteList = window.CooperanteList || {}, jQuery ));

(function( ProyectoList, $, undefined) {
  var tabla = $('#projecto-table').DataTable({
      dom: 'lfrtipB',
      buttons: ['excel','pdf'],
      processing: true,
      ajax: {
          url: $('#projectos-list-form').prop('action'),
          deferRender: true,
          dataSrc: '',
          cache: false,
          data: function () {
              return $('#projectos-list-form').serializeObject();
          }
      },
      columns: [
      {
          "data": "nombre",
          render: function (data, type, full) {
              return '<a href="'+full.url+'">'+full.nombre+'</a>';
          }
      },
      {
        data:"cantidad_equipamientos",className:"nowrap"
    }
    ]
}).on('xhr.dt', function () {
 $('#spinner').hide();
});;

  // Public
  ProyectoList.init = function () {
      $('#spinner').hide();
      $('#projectos-list-form').submit(function (e) {
          e.preventDefault();
          tabla.clear().draw();
          $('#spinner').show();
          tabla.ajax.reload();
      });

  }

}( window.ProyectoList = window.ProyectoList || {}, jQuery ));


(function( CooperanteMapa, $, undefined) {
    CooperanteMapa.ejecutar = function () {
        queue()
        .defer(d3.json, $('.origen-de-datos').data('url'))
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
                d["lng"] = +d["coordenadas"]["lng"];
                d["lat"] = +d["coordenadas"]["lat"];
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
                var markerCluster = L.markerClusterGroup({
                    chunkedLoading: true
                });

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

    }

  // Public
  CooperanteMapa.init = function () {
      CooperanteMapa.ejecutar();
  }

}( window.CooperanteMapa = window.CooperanteMapa || {}, jQuery ));