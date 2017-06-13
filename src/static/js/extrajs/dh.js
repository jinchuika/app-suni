(function( CalendarioDH, $, undefined ) {
    var crear_evento_dh_calendario = function () {
        $('#evento_dh-calendario').fullCalendar({
            header: {
                left: 'prev,next today,month,listYear',
                center: '',
                right: 'title'
            },

            navLinks: true, 
            eventSources: [
            {
                url: $('#evento_dh-calendario').data('url-evento_dh'),
                type: 'GET',
                cache: true,
            }
            ]
        });
    }

    CalendarioDH.init = function () {
        if ($('#evento_dh-calendario').length) {
            crear_evento_dh_calendario();
        }
    }
}( window.CalendarioDH = window.CalendarioDH || {}, jQuery ));

(function( ReservacionesDH, $, undefined ) {
    ReservacionesDH.init = function () {
        var tabla = $('.tabla-informe').DataTable({
            dom: 'lfrtipB',
            buttons: ['excel','pdf'],
        });
    }
}( window.ReservacionesDH = window.ReservacionesDH || {}, jQuery ));