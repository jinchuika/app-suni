(function( ReparacionDetalle, $, undefined ) {

    // Public
    ReparacionDetalle.init = function () {
        $('.form-nueva-reparacion').hide();
        $('#repuesto-nuevo-form').hide();
        $('#repuesto-nuevo-button').on('click', function () {
            $('#repuesto-nuevo-form').toggle();
        })
    }
}( window.ReparacionDetalle = window.ReparacionDetalle || {}, jQuery ));


(function( EquipamientoList, $, undefined ) {
    var tabla = $('#equipamiento-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#equipamiento-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#equipamiento-list-form').serializeObject(true);
            }
        },
        columns: [
        {
            data: "entrega",
            render: function ( data, type, full, meta ) {
                return '<a href="' + full.entrega_url + '">' + data + '</a>';
            }
        },
        {
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + full.escuela_url + '">' + data + '<br>(' + full.escuela_codigo + ')</a>';
            }
        },
        {"data": "fecha", "className": "nowrap"  },
        {"data": "renovacion" },
        {"data": "khan" },
        {"data": "cantidad" },
        {"data": "tipo_red" },
        {
            data: "cooperante",
            render: function (data, type, full, meta) {
                return data.map(function (cooperante) {
                    return '<a href="' + cooperante.url + '">' + cooperante.nombre + '</a>';
                }).join(', <br>');
            }
        },
        {
            data: "proyecto",
            render: function (data, type, full, meta) {
                return data.map(function (proyecto) {
                    return '<a href="' + proyecto.url + '">' + proyecto.nombre + '</a>';
                }).join(', <br>');
            }
        },
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    EquipamientoList.init = function () {
        $('#spinner').hide();
        $('#equipamiento-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
        $('#equipamiento-list-form #id_departamento').on('change', function () {
            listar_municipio_departamento('#equipamiento-list-form #id_departamento', '#equipamiento-list-form #id_municipio', true);
        });
    }
}( window.EquipamientoList = window.EquipamientoList || {}, jQuery ));

(function( EquipamientoInforme, $, undefined ) {
    var tabla = $('#equipamiento-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#equipamiento-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#equipamiento-list-form').serializeObject();
            }
        },
        columns: [
        {
            data: "entrega",
            render: function ( data, type, full, meta ) {
                return '<a href="' + full.entrega_url + '">' + data + '</a>';
            }
        },
        {
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + full.escuela_url + '">' + data + '</a>';
            }
        },
        { "data": "escuela_codigo", "className": "nowrap"  },
        { "data": "departamento"},
        { "data": "municipio"},
        { "data": "direccion" },
        { "data": "fecha", "className": "nowrap" },
        { "data": "renovacion"},
        { "data": "khan"},
        { "data": "cantidad"},
        { "data": "tipo_red"},
        {
            data: "cooperante",
            render: function (data, type, full, meta) {
                return data.map(function (cooperante) {
                    return '<a href="' + cooperante.url + '">' + cooperante.nombre + '</a>';
                }).join(', <br>');
            }
        },
        {
            data: "proyecto",
            render: function (data, type, full, meta) {
                return data.map(function (proyecto) {
                    return '<a href="' + proyecto.url + '">' + proyecto.nombre + '</a>';
                }).join(', <br>');
            }
        },
        { "data": "alumnas"},
        { "data": "alumnos"},
        { "data": "total_alumnos"},
        { "data": "maestras"},
        { "data": "maestros"},
        { "data": "total_maestros"},
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    EquipamientoInforme.init = function () {
        $('#spinner').hide();
        $('#equipamiento-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
        $('#equipamiento-list-form #id_departamento').on('change', function () {
            listar_municipio_departamento('#equipamiento-list-form #id_departamento', '#equipamiento-list-form #id_municipio', true);
        });
    }
}( window.EquipamientoInforme = window.EquipamientoInforme || {}, jQuery ));

(function( MonitoreoList, $, undefined ) {
    var tablaHabilitada = false;
    var tabla = $('#monitoreo-table').DataTable({
        paging:   false,
        dom: 'lfrtipB',
        processing: true,
        deferLoading: 0,
        buttons: ['excel','pdf'],
        ajax: {
            url: $('#monitoreo-list-form').attr('action'),
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#monitoreo-list-form').serializeObject();
            }
        },
        preDrawCallback: function () {
            return tablaHabilitada;
        },
        columns: [
        {data: "departamento"},
        {data: "municipio"},
        {
            targets: 1,
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + full.escuela_url + '">' + data + '<br>(' + full.escuela_codigo + ')</a>';
            }
        },
        {data: "entrega"},
        {data: "fecha", "className": "nowrap"},
        {data: "comentario"},
        ],
    });

    var filtro_list = [];

    // Public
    MonitoreoList.init = function () {
        $('#monitoreo-list-form').submit(function (e) {
            e.preventDefault();

            filtro_list = [];
            tabla.clear().draw();
            $('#spinner').show();

            $("#monitoreo-list-form :input").not(':submit,:button,:hidden').each(function() {
                if($(this).val() != ""){
                    filtro_list.push(1);
                }
            });

            if (filtro_list.length > 0) {
                tablaHabilitada = true;
                $('#span-filtros').remove();
                $('#spinner').show();
                tabla.clear().draw();
                tabla.ajax.reload();
            }
            else{
                tablaHabilitada = false;
                $('#monitoreo-list-form').append('<span id="span-filtros">Seleccione al menos un filtro</span>');
                $('#spinner').hide();
            }

        });

    }
}( window.MonitoreoList = window.MonitoreoList || {}, jQuery ));

(function( EquipamientoMapa, $, undefined ) {
    var map;
    var icono =  'http://funsepa.net/suni/media/ico3.png';

    var nuevo_marcador = function(lat, lng, info_text) {
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            icon: icono,
            animation: google.maps.Animation.DROP
        });
        var info_window = new google.maps.InfoWindow({content: info_text});
        google.maps.event.addListener(marker, 'mouseover', function() {info_window.open(map, marker);});
        google.maps.event.addListener(marker, 'mouseout', function() {info_window.close();});
    }

    var buscar_equipamiento = function(page) {
        page = (typeof page !== 'undefined') ?  page : 1;
        $.ajax({
            url: '',
            data: {
                page: page
            },
            method: 'post',
            dataType: 'json',
            success: function (response) {
                $.each(response.data, function(i, entry){
                    nuevo_marcador(entry.lat,entry.lng,entry.info);
                });
                if (response.next) {
                    buscar_equipamiento(response.page);
                }
            }
        });
    }

    // Public
    EquipamientoMapa.init = function () {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( {'address' : 'Guatemala'}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
            }
        });

        var mapOptions = {
            zoom:8,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            panControl: false,
            scaleControl: false,
            streetViewControl: false,
            scaleControl: false,
            scrollwheel: false
        }

        var styles = [{
            stylers: [
            { hue: "#128ab5" },
            { saturation: 82 }
            ]
        },{
            featureType: "road",
            elementType: "geometry",
            stylers: [
            { lightness: 19 },
            { visibility: "off" }
            ]
        },{
            featureType: "road",
            elementType: "labels",
            stylers: [
            { visibility: "off" }
            ]
        }];

        map = new google.maps.Map(document.getElementById("map"), mapOptions);
        map.setOptions({styles: styles});
        buscar_equipamiento();
    }
}( window.EquipamientoMapa = window.EquipamientoMapa || {}, jQuery ));

(function( DetalleGarantia, $, undefined ) {
  var tabla;
    var form_footer = [{
        style: 'tableExample',
        table: {
            widths: ['auto', 200, 'auto'],
            body: [
            [{text: 'Entrega', bold: true}, {text: '____________________________', alignment: 'center'},''],
            ['', {text: 'Nombre y firma', alignment:'center'}, {text: '',}],
            ['', '', {text: 'Sellos',}],
            [{text: 'Recibe', bold: true},{text: '____________________________', alignment: 'center'}, ''],
            ['', {text: 'Nombre y firma', alignment:'center'}, '']
            ]
        },
        layout: 'noBorders'
    },
    {text: '', margin: [0, 20]},
    {text: '14 Av. 19-50 Complejo Ofibodega San Sebastián No. 36, Condado El Naranjo Zona 4 de Mixco. Guatemala, C.A.', alignment: 'center', fontSize: 9},
    {text: '2435-2739 / 2435-9639', alignment: 'center', fontSize: 9},
    {text: 'info@funsepa.org   -    www.funsepa.org', alignment: 'center', fontSize: 9}
    ];

    var imprimir_detalle = function (url, ticket_id) {
        $.post(
            url,
            {ticket_id: ticket_id},
            function (data) {

                var reparacion_table = [[{text: 'Triage', style: 'tableHeader'}, {text: 'Dispositivo', style: 'tableHeader'}, {text: 'Problema reportado', style: 'tableHeader'}, {text: 'Problema encontrado', style: 'tableHeader'}]];
                for (var i = 0; i < data.reparaciones.length; i++) {
                    reparacion_table.push([
                        data.reparaciones[i].triage,
                        data.reparaciones[i].dispositivo,
                        data.reparaciones[i].falla_reportada,
                        data.reparaciones[i].falla_encontrada]);
                }
                var registro_table = [[{text: 'Registro', style: 'tableHeader'}, {text: 'Fecha', style: 'tableHeader'}, {text: 'Técnico a cargo', style: 'tableHeader'}]];
                for (var i = 0; i < data.registros.length; i++) {
                    registro_table.push([
                        data.registros[i].tipo,
                        data.registros[i].fecha,
                        data.registros[i].usuario]);
                }
                var dd = {

                    content: [
                    {text: 'Detalle de garantía', style: 'header', alignment: 'center'},
                    {
                        style: 'tableExample',
                        table: {
                            headerRows: 1,
                            body: [
                            [
                            {text: 'Escuela', bold: true}, data.escuela,
                            {text: 'Garantía', bold: true}, data.garantia,
                            {text: 'Ticket', bold:true}, data.ticket
                            ],
                            ]
                        },
                        layout: 'lightHorizontalLines'
                    },
                    {
                        style: 'tableExample',
                        table: {
                            headerRows: 1,
                            body: registro_table
                        },
                        layout: 'headerLineOnly'
                    },
                    {
                        style: 'tableExample',
                        table: {
                            headerRows: 1,
                            body: reparacion_table
                        },
                        layout: 'lightHorizontalLines',
                        alignment: 'justify'
                    },
                    {
                        style: 'tableExample',
                        table: {
                            body: [[{text: 'Descripción', bold: true}, data.descripcion],]
                        },
                        layout: 'lightHorizontalLines',
                    },
                    form_footer
                    ],
                    styles: {
                        header: {
                            fontSize: 18,
                            bold: true,
                            margin: [0, 0, 0, 10]
                        },
                        tableExample: {
                            margin: [0, 5, 0, 15],
                            fontSize: 10
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'black'
                        }
                    }
                }
                //pdfMake.createPdf(dd).download();
            });
}


    var imprimir_registro = function (url, ticket_id) {
        $.post(
            url,
            {ticket_id: ticket_id},
            function (data) {
                var dd = {
                    content: [
                    {text: 'Formulario de visita técnica', style: 'header', alignment: 'center'},
                    {
                        style: 'tableExample',
                        table: {
                            headerRows: 1,
                            body: [
                            [
                            {text: 'Escuela', bold: true}, data.escuela,
                            {text: 'Garantía', bold: true}, data.garantia,
                            {text: 'Ticket', bold:true}, data.ticket
                            ],
                            ]
                        },
                        layout: 'lightHorizontalLines'
                    },
                    {
                        style: 'tableExample',
                        table: {
                            widths: ['auto', 50, 50, 300, 'auto'],
                            headerRows: 1,
                            body: [
                            ['No.', 'Tipo', 'Triage', 'Problema que presenta y solucion', 'Resuelto'],
                            ['\n1', '', '', '', ''],
                            ['\n2', '', '', '', ''],
                            ['\n3', '', '', '', ''],
                            ['\n4', '', '', '', ''],
                            ['\n5', '', '', '', ''],
                            ['\n6', '', '', '', ''],
                            ['\n7', '', '', '', ''],
                            ['\n8', '', '', '', ''],
                            ['\n9', '', '', '', ''],
                            ['\n10', '', '', '', ''],
                            ]
                        },
                    },
                    {
                        style: 'tableExample',
                        table: {
                            body: [
                            [{text: 'Descripción', bold: true}, data.descripcion],
                            [{text: 'Observaciones', bold: true}, ''],
                            ]
                        },
                        layout: 'lightHorizontalLines',
                    },
                    form_footer
                    ],
                    styles: {
                        header: {
                            fontSize: 18,
                            bold: true,
                            margin: [0, 0, 0, 10]
                        },
                        tableExample: {
                            margin: [0, 5, 0, 15],
                            fontSize: 10
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'black'
                        }
                    }
                }
                pdfMake.createPdf(dd).download();
            }
            );
    }

    //var imprimir_monitoreo_visitas = function (url, id_visita){
      var imprimir_monitoreo_visitas = function (){

    /*  $.post(
        url,
        {id_visita : id_visita},
        function (data){

          var cuerpo ={
            content: [
              {
                text:'Detalle de Visitas Monitoreadas', style: 'header', alignment:'center'
              },
              {
                style:'tableExample',
                table:{
                  headerRows:1,
                  body:[
                    [
                      {text: 'Encargado'},data.Encargado,
                      {text: 'Escuela'},data.Escuela,
                      {text: 'Direccion'},data.Direccion,
                      {text: 'Equipamiento'},data.Equipamiento,
                      {text: 'Fecha de Visita'},data.FechaDeVisita,
                      {text: 'Hora de Inicio'},data.HorarioInicial,
                      {text: 'Hora Final'},data.HorarioFinal,
                      {text: 'Contacto'},data.Contacto,


                    ]
                  ]
                }
              }
            ]
          }

            pdfMake.createPdf(cuerpo).download();
        }

      );*/
    }

    // Public
    DetalleGarantia.init = function () {
        $('#form-nuevo-ticket').hide();
        $('.form-nuevo-registro').hide();
        $('.form-nuevo-transporte').hide();
        $('#button-nuevo-ticket').on('click', function () {
          $('#form-nuevo-ticket').toggle();
      });

        $('.btn-print-ticket').on('click', function () {
            imprimir_detalle($(this).data('url'), $(this).data('ticket'));
        });

        $('.btn-print-registro').on('click', function () {
            imprimir_registro($(this).data('url'), $(this).data('ticket'));
        })
         tabla = $('#visita-table').DataTable({
          dom: 'lfrtipB',
          buttons: ['excel', 'pdf'],
          processing:true,          
        }).on('xhr.dt',function(e, settings, json, xhr){
          $('#spinner').hide();
        });
        $('spinner').hide();

    }
}( window.DetalleGarantia = window.DetalleGarantia || {}, jQuery ));


(function( ReparacionList, $, undefined ) {
    var tabla;

    // Public
    ReparacionList.init = function () {
        tabla = $('#reparacion-table').DataTable({
            dom: 'lfrtipB',
            buttons: ['excel','pdf'],
            processing: true,
            ajax: {
                url: "",
                type: "POST",
                deferRender: true,
                dataSrc: '',
                data: function () {
                    return $('#reparacion-list-form').serializeObject();
                }
            },
            columns: [
            { "data": "ticket"},
            { "data": "triage"},
            { "data": "dispositivo" },
            { "data": "fecha_inicio", "className": "nowrap" },
            { "data": "falla_reportada" },
            { "data": "escuela" },
            ]
        }).on('xhr.dt', function (e, settings, json, xhr) {
            $('#spinner').hide();
        });

        $('#spinner').hide();
        $('#reparacion-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    }
}( window.ReparacionList = window.ReparacionList || {}, jQuery ));


(function( TicketInforme, $, undefined ) {
    var tabla = $('#ticket-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#ticket-list-form').serializeObject();
            }
        },
        columns: [
        {data: "no_ticket"},
        {data: "entrega"},
        {
            data: "escuela",
            render: function (data) {
                return '<a href="' + data.url + '">' + data.nombre + '<br>(' + data.codigo + ')</a>';
            }
        },
        {data: "fecha_inicio", "className": "nowrap", type: "date"},
        {data: "fecha_fin", "className": "nowrap"},
        {data: "estado" },
        {data: "costo_reparacion", type: "num"},
        {data: "costo_transporte", type: "num"},
        {data: "costo_total", type: "num"},
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    TicketInforme.init = function () {
        console.log("hola");
        $('#spinner').hide();
        $('#ticket-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    }
}( window.TicketInforme = window.TicketInforme || {}, jQuery ));

(function( TicketReparacionInforme, $, undefined ) {
    var tabla = $('#ticket-reparacion-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#ticket-list-form').serializeObject();
            }
        },
        columns: [
        {data: "no_ticket"},
        {
            data: "triage",
            render: function (data) {
                return '<a href="' + data.url + '">' + data.triage + '</a>';
            },
            className: "nowrap"
        },
        {data: "entrega"},
        {
            data: "escuela",
            render: function (data) {
                return '<a href="' + data.url + '">' + data.nombre + '<br>(' + data.codigo + ')</a>';
            }
        },
        {data: "fecha_inicio", "className": "nowrap", type: "date"},
        {data: "fecha_fin", "className": "nowrap"},
        {data: "falla_reportada" },
        {data: "falla_encontrada" },
        {data: "solucion_detalle" },
        {data: "estado" },
        {data: "tecnico_asignado"},
        {
            data: "cooperante",
            render: function (data, type, full, meta) {
                return data.map(function (cooperante) {
                    return '<a href="' + cooperante.url + '">' + cooperante.nombre + '</a>';
                }).join(', <br>');
            }
        },
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    TicketReparacionInforme.init = function () {
        $('#spinner').hide();
        $('#ticket-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

    }
}( window.TicketReparacionInforme = window.TicketReparacionInforme || {}, jQuery ));


(function( CalendarioTPE, $, undefined ) {
    var crear_equipamiento_calendario = function () {
        $('#tpe-calendario').fullCalendar({
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
                        text: event.tip_text,

                    },
                });
            },
            eventSources: [
            {
                url: $('#tpe-calendario').data('url-validacion'),
                type: 'GET',
                color: 'orange',
                cache: true,
            },
            {
                url: $('#tpe-calendario').data('url-equipamiento'),
                type: 'GET',
                color: 'green',
                cache: true,
            },
            {
                url: $('#tpe-calendario').data('url-ticket'),
                type: 'GET',
                cache: true,
            },
            {
                url: $('#tpe-calendario').data('url-visita'),
                type: 'GET',
                color: 'red',
                cache: true,
            },
            ]
        });
    }

    // Public
    CalendarioTPE.init = function () {
        $('#spinner').hide();
        crear_equipamiento_calendario();
    }
}( window.CalendarioTPE = window.CalendarioTPE || {}, jQuery ));


(function( EvaluacionMonitoreo, $, undefined ) {

    // Public
    EvaluacionMonitoreo.init = function () {
        $('#evaluacion-form').on('submit', function (e) {
            e.preventDefault();
            var data = [];
            $.each($('.punteo'), function (index, item) {
                $.ajax({
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                    },
                    url: $(item).data('url'),
                    data: {'punteo': $(item).val()},
                    type: 'post',
                    dataType: 'json',
                    success: function (resultado) {
                        $('#evaluacion-'+resultado.id).html(resultado.porcentaje);
                    }
                });
            });
            console.log(data);
        })
    }
}( window.EvaluacionMonitoreo = window.ReparacionDetalle || {}, jQuery ));

(function( EvaluacionMonitoreoList, $, undefined ) {
    var tabla = $('#evaluacionmonitoreo-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#evaluacionmonitoreo-list-form').prop('action'),
            deferRender: true,
            cache: false,
            dataSrc: '',
            data: function () {
                return $('#evaluacionmonitoreo-list-form').serializeObject();
            }
        },
        columns: [
        {
            "data": "escuela",
            render: function (data) {
                return '<a href="'+data.url+'">'+data.nombre+'<br>('+data.codigo+')</a>';
            }
        },
        {"data": "equipamiento"},
        {"data": "fecha_equipamiento", "className": "nowrap"},
        {"data": "pregunta"},
        {"data": "creado_por"},
        {"data": "fecha", "className": "nowrap"},
        {"data": "porcentaje"},
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#evaluacionmonitoreo-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
         $('#spinner').hide();
    });

    // Public
    EvaluacionMonitoreoList.init = function () {
        $('#spinner').hide();
        $('#evaluacionmonitoreo-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
    }
}( window.EvaluacionMonitoreoList = window.EvaluacionMonitoreoList || {}, jQuery ));


(function( DispositivoReparacion, $, undefined ) {
    var tabla = $('#dispositivo-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#dispositivo-list-form').prop('action'),
            deferRender: true,
            cache: false,
            dataSrc: '',
            data: function () {
                return $('#dispositivo-list-form').serializeObject();
            }
        },
        columns: [
        {"data": "tipo"},
        {"data": "total"}
        ]
    })
    .on('xhr.dt', function (e, settings, json, xhr) {
        $('#dispositivo-table tbody tr').each(function(index, item){
            $(item).find('td:eq(5)').attr('nowrap', 'nowrap');
        });
         $('#spinner').hide();
    });

    // Public
    DispositivoReparacion.init = function () {
        $('#spinner').hide();
        $('#dispositivo-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
    }
}( window.DispositivoReparacion = window.DispositivoReparacion || {}, jQuery ));
