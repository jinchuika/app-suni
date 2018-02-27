(function( CalendarioNaat, $, undefined ) {

    var crear_naat_calendario = function () {
        var naat_calendario = $('#naat-calendario');
        naat_calendario.fullCalendar({
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
                    }
                });
            },
            eventSources: [{
                url: naat_calendario.data('url-calendario'),
                type: 'GET',
                color: 'orange',
                cache: true,
                data: function () {
                    return $('#calendario-form').serializeObject();
                }
            }]
        });
    };

    // Public
    CalendarioNaat.init = function () {
        crear_naat_calendario();
        $('#id_capacitador').on('change', function(){
            $('#naat-calendario').fullCalendar( 'refetchEvents' );
        })
    }
}( window.CalendarioNaat = window.CalendarioNaat || {}, jQuery ));