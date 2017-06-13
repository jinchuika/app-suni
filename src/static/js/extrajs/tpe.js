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
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#equipamiento-list-form').serializeObject();
            }
        },
        columns: [
        {"data": "entrega"},
        {"data": "escuela"},
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
        ],
        "columnDefs": [
        {
            targets: 0,
            data: "entrega",
            render: function ( data, type, full, meta ) {
                return '<a href="' + full.entrega_url + '">' + data + '</a>';
            }
        },
        {
            targets: 1,
            data: "escuela",
            render: function (data, type, full, meta) {
                return '<a href="' + full.escuela_url + '">' + data + '<br>(' + full.escuela_codigo + ')</a>';
            }
        }
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

    } 
}( window.EquipamientoList = window.EquipamientoList || {}, jQuery ));

(function( EquipamientoInforme, $, undefined ) {
    var tabla = $('#equipamiento-informe-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: "",
            type: "POST",
            deferRender: true,
            dataSrc: '',
            data: function () {
                return $('#equipamiento-list-form').serializeObject();
            }
        },
        columns: [
        { "data": "entrega"},
        { "data": "escuela"},
        { "data": "codigo", "className": "nowrap"  },
        { "data": "departamento"},
        { "data": "municipio"},
        { "data": "direccion" },
        { "data": "fecha", "className": "nowrap" },
        { "data": "renovacion"},
        { "data": "khan"},
        { "data": "cantidad"},
        { "data": "tipo_red"},
        { "data": "cooperante", 'render': '[, <br>].cooperante'},
        { "data": "proyecto", 'render': '[, <br>].proyecto'},
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

    } 
}( window.EquipamientoInforme = window.EquipamientoInforme || {}, jQuery ));

(function( MonitoreoList, $, undefined ) {
    var tabla = $('#monitoreo-table').DataTable({
        "paging":   false,
        rowsGroup: [
        3, 2, 0, 1
        ],
    });
    var armar_tabla = function (monitoreo_list) {
        $.each(monitoreo_list, function (index, equipamiento) {
            tabla.row.add([
                equipamiento.departamento,
                equipamiento.municipio,
                equipamiento.escuela,
                equipamiento.entrega,
                equipamiento.fecha,
                equipamiento.comentario
                ]).draw(false);
        });
    }

    // Public
    MonitoreoList.init = function () {
        $('#monitoreo-list-form').submit(function (e) {
            e.preventDefault();
            tabla.clear().draw();
            $.ajax({
                type: 'post',
                url: $(this).attr('action'),
                dataType: 'json',
                data: $(this).serialize(),
                success: function (respuesta) {
                    armar_tabla(respuesta);
                }
            });
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
                pdfMake.createPdf(dd).download();
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
