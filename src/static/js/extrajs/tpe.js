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
    var marcadores = [];
    var infos = [];
    var icono =  'http://funsepa.net/suni/media/ico3.png';
    var cont = 0;
    function nuevo_marcador(lat,lng,info) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            icon: icono,
            animation: google.maps.Animation.DROP
        });
        infos.push(new google.maps.InfoWindow({content: info}));
        marcadores.push(marker);
        cont = cont + 1;
    }

    function mostrar_marcadores (mapa) {
        for (var i = 0; i < marcadores.length; i++) {
            marcadores[i].setMap(mapa);
        }
    }

    function crear_mapa() {
        var country = "Guatemala";
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( {'address' : country}, function(results, status) {
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
        mapa_temp = new Array();
        
        $.post("", function (json) {
            $.each(json, function(i, entry){
                nuevo_marcador(entry.lat,entry.lng,entry.info);
                mapa_temp.push(new google.maps.LatLng(entry.lat,entry.lng));
            });
            $.each(infos, function (i, info) {
                google.maps.event.addListener(marcadores[i], 'mouseover', function() {info.open(map,marcadores[i]);});
                google.maps.event.addListener(marcadores[i], 'mouseout', function() {info.close();});
            });
            document.getElementById('cantidad').innerHTML = json.length+ ' Equipamientos';
        });

        var pointArray = new google.maps.MVCArray(mapa_temp);
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: pointArray,
            radius: 25
        });

        var gradient = [
        'rgba(0, 255, 255, 0)',
        'rgba(0, 255, 255, 1)',
        'rgba(0, 191, 255, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(0, 63, 255, 1)',
        'rgba(0, 0, 255, 1)',
        'rgba(0, 0, 223, 1)',
        'rgba(0, 0, 191, 1)',
        'rgba(0, 0, 159, 1)',
        'rgba(0, 0, 127, 1)',
        'rgba(63, 0, 91, 1)',
        'rgba(127, 0, 63, 1)',
        'rgba(191, 0, 31, 1)',
        'rgba(255, 0, 0, 1)'
        ]
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
        heatmap.setMap(map);
        heatmap.setMap(heatmap.getMap() ? null : map);

        var control_tendencia_div = document.createElement('div');
        var controlTendencia = new control_tendencia(control_tendencia_div, map);

        control_tendencia_div.index = 1;
        map.controls[google.maps.ControlPosition.TOP_RIGHT].push(control_tendencia_div);
    }

    // Public
    EquipamientoMapa.init = function () {
        $(document).ready(function () {
            crear_mapa();
        })
    }   
}( window.EquipamientoMapa = window.EquipamientoMapa || {}, jQuery ));
