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



class tareasNaat{
    constructor(){
        $('#tareas-naat-list-form').on('submit', function(e) {
        e.preventDefault(); 
        var sede = $('#id_sede').val();
        var url_api = $('#tareasNaat').data('url');
        $('#tbody-tareas').html('<tr><td colspan="6" class="text-center">Cargando tareas...</td></tr>');

        $.ajax({
            url: url_api,
            type: 'GET',
            data: { 'sede': sede },
            success: function(response) {
                var tbody = $('#tbody-tareas');
                tbody.empty();

                if(response.error) {
                    tbody.append('<tr><td colspan="6" class="text-center text-danger">' + response.error + '</td></tr>');
                    return;
                }

                if(response.length === 0) {
                    tbody.append('<tr><td colspan="6" class="text-center">No hay maestros con tareas para esta sede</td></tr>');
                    return;
                }

                var maestrosNoRegistrados = 0;
                $.each(response, function(index, maestro) {
                    if (maestro.registrado === false) {
                        maestrosNoRegistrados++;
                    }
                });

                if (maestrosNoRegistrados > 0) {
                    bootbox.alert({
                        message: "<h3><i class='fa fa-exclamation-triangle'></i> Atención</h3><br>Se encontraron <strong>" + maestrosNoRegistrados + "</strong> maestro(s) en esta sede que tienen tareas en NAAT pero <strong>NO están registrados en el sistema SUNI</strong>. Verifique los datos.",
                        className: "modal modal-warning fade"
                    });
                }

                $.each(response, function(index, maestro) {
                    var tr = $('<tr></tr>');
                    if (maestro.registrado) {
                        tr.append('<td><a href="' + maestro.url_participante + '" target="_blank" class="text-primary"><strong>' + maestro.nombre + '</strong></a></td>');
                    } else {
                        tr.append('<td class="text-danger"><strong>' + maestro.nombre + '</strong></td>');
                    }
                    
                    tr.append('<td>' + maestro.apellido + '</td>');

                    var nombres_tareas = [
                        "Evaluación final M1", 
                        "Evaluación final del módulo 2", 
                        "Aulas colaborativas", 
                        "Evaluación final del módulo 4" 
                    ];

                    $.each(nombres_tareas, function(i, nombre_t) {
                        var td = $('<td class="text-center"></td>');
                        
                        if (maestro.tareas && maestro.tareas[nombre_t]) {
                            var ruta = maestro.tareas[nombre_t];
                            var btn = $('<button class="btn btn-info btn-sm btn-ver-tarea" title="Ver tarea"><i class="fa fa-eye"></i></button>');
                            btn.data('ruta', ruta);
                            btn.data('nombre', nombre_t);
                            td.append(btn);
                        } else {
                            td.append('<span class="text-muted">-</span>');
                        }
                        tr.append(td);
                    });

                    tbody.append(tr);
                });
            },
            error: function() {
                $('#tbody-tareas').html('<tr><td colspan="6" class="text-center text-danger">Error de conexión</td></tr>');
            }
        });
    });

    $(document).on('click', '.btn-ver-tarea', function() {
        var ruta_pdf = $(this).data('ruta');
        var nombre_tarea = $(this).data('nombre');
        
        $('#tituloTarea').text(nombre_tarea);
        $('#iframeTarea').attr('src', ruta_pdf); 
        $('#modalVerTarea').modal('show'); 
    });

    $('#modalVerTarea').on('hidden.bs.modal', function () {
        $('#iframeTarea').attr('src', '');
    });
    };
}



class informeParticipantesNaat {
    constructor() {
        $('#informeParticipanteNaat-list-form').on('submit', function(e) {
            e.preventDefault(); 
            var url_api = $(this).attr('action');
            $('#informeParticipanteNaat-body').html('<tr><td colspan="15" class="text-center">Cargando informe...</td></tr>');

            var tablaRastreo = $('#informeParticipanteNaat-table').DataTable({
                dom: 'lfrtipB',
                buttons: ['excel', 'pdf', 'copy'],
                searching: true,
                paging: false,
                ordering: true,
                processing: true,
                traditional: true,
                destroy: true, 
                ajax: {
                    url: url_api, 
                    dataSrc: '',
                    cache: false,
                    type: 'GET',
                    error: function(jqXHR, textStatus, errorThrown) {          
                        if(jqXHR.responseText) {
                            var responseJSON = JSON.parse(jqXHR.responseText);
                            bootbox.alert({ message: "<h2>"+responseJSON["error"]+"</h2>", className:"modal modal-info fade in" });
                        } else {
                            bootbox.alert({ message: "<h2>Error de conexión</h2>", className:"modal modal-danger fade in" });
                        }
                    },
                    data: function (d) {
                        d.sede = $('#id_sede').val();
                        d.fecha_inicio = $('#id_fecha_min').val();
                        d.fecha_fin = $('#id_fecha_max').val();
                    }
                },
                columns: [
                    {data: "nombre", defaultContent: ""},
                    {data: "apellido", defaultContent: ""},
                    {data: "udi", defaultContent: ""},
                    {data: "municipio", defaultContent: ""},
                    {data: "departamento", defaultContent: ""},
                    {data: "puesto", defaultContent: ""},
                    
                    {data: "mundo1", defaultContent: "-", className: "text-center"},
                    {data: "mundo1_pc_nota_inicial", defaultContent: "-", className: "text-center"},
                    {data: "mundo1_pc_nota_final", defaultContent: "-", className: "text-center"},
                    
                    {data: "mundo2", defaultContent: "-", className: "text-center"},
                    {data: "mundo2_pc_nota_inicial", defaultContent: "-", className: "text-center"},
                    {data: "mundo2_pc_nota_final", defaultContent: "-", className: "text-center"},
                    
                    {data: "mundo3", defaultContent: "-", className: "text-center"},
                    {data: "mundo3_pc_nota_inicial", defaultContent: "-", className: "text-center"},
                    {data: "mundo3_pc_nota_final", defaultContent: "-", className: "text-center"},
                    
                    {data: "mundo4", defaultContent: "-", className: "text-center"},
                    {data: "mundo4_pc_nota_inicial", defaultContent: "-", className: "text-center"},
                    {data: "mundo4_pc_nota_final", defaultContent: "-", className: "text-center"},

                    {data: "mundo5", defaultContent: "-", className: "text-center"},
                    {data: "mundo6", defaultContent: "-", className: "text-center"},
                    {data: "mundo7", defaultContent: "-", className: "text-center"},
                    {data: "mundo8", defaultContent: "-", className: "text-center"},

                ]
            });
        });
    }
}
