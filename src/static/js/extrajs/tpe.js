(function( DetalleGarantia, $, undefined ) {

    // Public
    DetalleGarantia.init = function () {
    	$('#form-nuevo-ticket').hide();
    	$('.form-nuevo-registro').hide();
    	$('#button-nuevo-ticket').on('click', function () {
    		$('#form-nuevo-ticket').toggle();
    	});

    }   
}( window.DetalleGarantia = window.DetalleGarantia || {}, jQuery ));

(function( ReparacionDetalle, $, undefined ) {

    // Public
    ReparacionDetalle.init = function () {
        $('.form-nueva-reparacion').hide();

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
        { "data": "entrega"},
        { "data": "escuela"},
        { "data": "fecha", "className": "nowrap"  },
        { "data": "renovacion" },
        { "data": "khan" },
        { "data": "cantidad" },
        { "data": "tipo_red" },
        { "data": "cooperante", 'render': '[, <br>].cooperante' },
        { "data": "proyecto", 'render': '[, <br>].proyecto' },
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