class Informe {
  constructor() {
    $('#informe-list-form').submit(function (e) {
            // Evita que se envíe el formulario
            e.preventDefault();
            var tabla = $('#informe-table').DataTable({
            dom: 'lfrtipB',
            buttons: ['excel','pdf'],
            searching:true,
            paging:true,
            ordering:true,
            processing:true,
            destroy:true,
            ajax: {
                url: $('#informe-list-form').attr('action'),
                type: "GET",
                deferRender: true,
                dataSrc: '',
                data: function () {
                    return $('#informe-list-form').serializeObject();
                }
            },
            columns: [
            {data: "Udi"},
            {
                data: "Nombre",
                render: function ( data, type, full, meta ) {
                    return '<a href="' + full.escuela_url + '">' + data + '</a>';
                }
            },
            {data: "Direccion"},
            {data: "Departamento"},
            {data: "Municipio"},
            {data: "Ninos_beneficiados"},
            {data: "Docentes"},
            {
                data: "Equipada",
                render: function (data) {

                    return data ? 'Sí' : 'No';
                }
            },
            {data: "Fecha_equipamiento"},
            {data: "No_equipamiento"},
            {data: "Proyecto"},
            {data: "Donante"},
            {data: "Equipo_entregado"},
            {
                data: "Capacitada",
                render: function (data) {

                    return data ? 'Sí' : 'No';
                }
            },
            {data: "Fecha_capacitacion"},
            {data: "Capacitador"},
            {data: "Maestros_capacitados"},
            {data: "Maestros_promovidos"},
            {data: "Maestros_no_promovidos"},
            {data: "Maestros_desertores"}

          ],
        });
        });
  }
}
