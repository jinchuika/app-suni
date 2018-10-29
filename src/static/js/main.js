$(document).ajaxStart(function() { Pace.restart(); });

!function(a){a.fn.datepicker.dates.es={days:["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"],daysShort:["Dom","Lun","Mar","Mié","Jue","Vie","Sáb"],daysMin:["Do","Lu","Ma","Mi","Ju","Vi","Sa"],months:["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],monthsShort:["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],today:"Hoy",monthsTitle:"Meses",clear:"Borrar",weekStart:1,format:"dd/mm/yyyy"}}(jQuery);

function activar_tab(tab){
  $('.nav-tabs a[href="#' + tab + '"]').tab('show');
};

$.fn.serializeObject = function(not_null)
{
    var o = {};
    var array = this.serializeArray();
    $.each(array, function() {
        if (this.value) {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        }
    });
    return o;
};

function validar_udi(codigo) {
    return /^\d{2}-\d{2}-\d{4}-\d{2}$/.test(codigo);
}

function activar_datatable(tabla) {
    $(tabla).DataTable({
        "iDisplayLength": 50,
        "language":{
            "sProcessing":     "Procesando...",
            "sLengthMenu":     "Mostrar _MENU_ registros",
            "sZeroRecords":    "No se encontraron resultados",
            "sEmptyTable":     "Ningún dato disponible en esta tabla",
            "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix":    "",
            "sSearch":         "Buscar:",
            "sUrl":            "",
            "sInfoThousands":  ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst":    "Primero",
                "sLast":     "Último",
                "sNext":     "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        }
    });
}

function listar_municipio_departamento(departamento_selector, municipio_selector, null_option) {
    /*
    Al cambiar el departamento, genera el listado de municipios
    */
    $(municipio_selector).html('');
    $.get($(departamento_selector).data('url'),
    {
        departamento: $(departamento_selector).val()
    },
    function (respuesta) {
        var options = '';
        if (null_option) {
            options += '<option value="">---</option>';
        }
        $.each(respuesta, function (index, municipio) {
            options += '<option value="'+municipio.id+'">'+municipio.nombre+'</option>';
        });
        $(municipio_selector).html(options).trigger('change');
    });
}

$(document).ready(function () {
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        language: 'es'
    }).attr('onkeydown', 'return false');

    $.each($('.table-datatables'), function (index, tabla) {
        activar_datatable(tabla);
    });

    $(".select2").select2({
        width : '100%'
    });

    $('.datatable-simple'). DataTable({
        searching: false,
        lengthChange: false,
        info: false,
        pagingType: "simple",
        ordering: false,
        responsive: true,
        "language": {
            "oPaginate": {
                "sNext":     ">",
                "sPrevious": "<"
            },
        }
    });

    Noty.overrideDefaults({
        theme    : 'metroui',
    });
});