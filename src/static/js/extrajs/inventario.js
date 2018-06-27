(function (AlertaEnCreacion, $, undefined) {
    AlertaEnCreacion.init = function () {
        var mensaje = document.getElementById("id_en_creacion");
        $('#id_en_creacion').click(function () {
            if ($("#id_en_creacion").is(':checked')) {
                bootbox.alert("esta activado");
            } else {
                bootbox.alert("Esta Seguro que quiere Terminara la Creacion de la Entrada");
            }
        });


    }

}(window.AlertaEnCreacion = window.AlertaEnCreacion || {}, jQuery));

class EntradaUpdate {
    constructor() {
        let entrada_table = $('#entrada-table');

        this.api_url = entrada_table.data("api");
        this.pk = entrada_table.data("pk");
        this.url_filtrada = this.api_url + "?entrada=" + this.pk;
        this.tabla = entrada_table.DataTable({
            searching: false,
            paging: true,
            ordering: false,
            processing: true,
            ajax: {
                url: this.url_filtrada,
                dataSrc: '',
                cache: true,
                data: this.api_url
            },
            columns: [
                {data: "tdispositivo"},
                {data: "util"},
                {data: "repuesto"},
                {data: "desecho"},
                {data: "total"},
                {data: "precio_unitario"},
                {data: "precio_subtotal"},
                {data: "precio_descontado"},
                {data: "precio_total"},
                {data: "creado_por"},
                {
                    data: "",
                    defaultContent: "<button class='btn btn-info btn-editar'>Editar</button>", targets: -1
                },
                {
                    data: "",
                    defaultContent: "<button class='btn btn-primary btn-dispositivo'>Crear Disp</button>", targets: -1
                },
                {
                    data: "",
                    defaultContent: "<button class='btn btn-warning btn-repuesto'>Crear Rep</button>", targets: -1
                },
            ]
        });

        let tablabody = $('#entrada-table tbody');
        let tabla_temp = this;

        tablabody.on('click', '.btn-editar', function () {
            let data_fila = this.tabla.row($(this).parents('tr')).data();
            location.href = data_fila.update_url;
        });

        tablabody.on('click', '.btn-dispositivo', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_dispositivos/";
            EntradaUpdate.crear_dispositivos(urldispositivo);
        });

        tablabody.on('click', '.btn-repuesto', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_repuestos/";
            EntradaUpdate.crear_repuestos(urldispositivo);
        });

        /** Uso de DRF**/
        let detalle_form = $('#detalleForm');
        detalle_form.submit(function (e) {
            e.preventDefault();

            $.ajax({
                type: "POST",
                url: detalle_form.attr('action'),
                data: detalle_form.serialize(),
                success: function (response) {
                    console.log("datos ingresados correctamente");

                },
            });
            this.tabla.clear().draw();
            this.tabla.ajax.reload();
            document.getElementById("detalleForm").reset();
        });
    }

    static crear_dispositivos(urldispositivo) {
        $.ajax({
            type: 'POST',
            url: urldispositivo,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log("dispositivos creados exitosamente");
            },
            error: function (response) {
                alert(response.mensaje);
            }
        });
    }

    static crear_repuestos(url_repuestos) {
        $.ajax({
            type: 'POST',
            url: url_repuestos,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log("repuestos creados exitosamente");
            },
        });
    }
}


(function (EntradaList, $, undefined) {
    var tabla = $('#entrada2-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel', 'pdf'],
        processing: true,
        ajax: {
            url: $('#entrada2-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            cache: true,
            data: function () {
                return $('#entrada2-list-form').serializeObject(true);
            }
        },
        columns: [

            {data: "tipo"},
            {data: "fecha", className: "nowrap"},
            {data: "en_creacion", className: "nowrap"},
            {data: "creada_por", className: "nowrap"},
            {data: "recibida_por", className: "nowrap"},
            {data: "proveedor", className: "nowrap"},
            {data: "", defaultContent: "<button>Edit</button>", targets: -1}
        ]


    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    EntradaList.init = function () {

        $('#spinner').hide();
        $('#entrada2-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

        $('#entrada2-table tbody').on('click', 'button', function () {
            var data = tabla.row($(this).parents('tr')).data();
            alert("Si funciona este boton");
            console.log(data.fecha);
        });

    }
}(window.EntradaList = window.EntradaList || {}, jQuery));

(function (SalidaDetalleList, $, undefined) {
    var valor = $('#salida-table').data("api");
    var pk = $('#salida-table').data("pk");
    var urlapi = valor + "?entrada=" + pk;
    var tabla = $('#salida-table').DataTable({
        searching: false,
        paging: true,
        ordering: false,
        processing: true,
        ajax: {
            url: urlapi,
            dataSrc: '',
            cache: true,
            data: function () {
                var cont = $('#salida-table').data("api");
                return cont;
            }
        },
        columns: [
            {data: "tdispositivo"},
            {data: "cantidad"},
            {data: "desecho"},
            {data: "entrada_detalle"},
        ]
    });

    SalidaDetalleList.init = function () {
        $('#btn-terminar').click(function () {
            bootbox.confirm({
                message: "¿Esta Seguro que quiere Terminara la Creacion de la Entrada?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result == true) {
                        document.getElementById("id_en_creacion").checked = false;
                        document.getElementById("desechosalida-form").submit();
                    }

                }
            });


        });

        /** Uso de DRF**/
        $('#detalleForm').submit(function (e) {
            e.preventDefault()

            $.ajax({
                type: "POST",
                url: $('#detalleForm').attr('action'),
                data: $('#detalleForm').serialize(),
                success: function (response) {
                    console.log("datos ingresados correctamente");

                },
            });
            tabla.clear().draw();
            tabla.ajax.reload();
            document.getElementById("detalleForm").reset();
        });
    }
}(window.SalidaDetalleList = window.SalidaDetalleList || {}, jQuery));


class SolicitudMovimientoUpdate {
    constructor() {
        this.sel_dispositivos = $('#id_dispositivos');
        let api_url = this.sel_dispositivos.data('api-url');
        let etapa_inicial = this.sel_dispositivos.data('etapa-inicial');
        let tipo_dipositivo = this.sel_dispositivos.data('tipo-dispositivo');
        let slug = this.sel_dispositivos.data('slug');

        this.sel_dispositivos.select2({
            debug: true,
            placeholder: "Ingrese los triage",
            ajax: {
                url: api_url,
                dataType: 'json',
                data: function (params) {
                    return {
                        search: params.term,
                        etapa: etapa_inicial,
                        tipo: tipo_dipositivo,
                        buscador: slug + "-" + params.term
                    };
                },
                processResults: function (data) {
                    return {
                        results: data.map(dispositivo => {
                            return {id: dispositivo["id"], text: dispositivo['triage']};
                        })
                    };
                },
                cache: true
            },
            width : '100%'
        });
    }
}
