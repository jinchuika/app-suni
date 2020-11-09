class Informe {
  constructor() {
$( "#id_codigo" )
  .focusout(function() {
    var valor = $( "#id_codigo" ).val();
    var regex_udi = /\d{2}-\d{2}-\d{4}-\d{2}/;
    if(regex_udi.test(valor)){
      $('#boton_enviar').prop('disabled', false);
    }else{    
      bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + "Este Formato de UDI no es correco", className:"modal modal-danger fade"});
      $('#boton_enviar').prop('disabled', true);
    }
  }).blur(function() {
       $('#boton_enviar').prop('disabled', false);
  });

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
          footerCallback: function( tfoot, data, start, end, display){
              var api = this.api();
              var acumulador_ninos_beneficiados = 0;
              var acumulador_docentes = 0;
              var acumulador_equipo_entregado=0;
              var acumulador_maestros_capacitados=0;
              var acumulador_promovidos=0;
              var acumulador_no_promovidos=0;
              var acumulador_inconclusos=0;
              for (var i in data){
                //console.log(data[i].Ninos_beneficiados)

                acumulador_ninos_beneficiados= acumulador_ninos_beneficiados + data[i].Ninos_beneficiados;
                acumulador_docentes = acumulador_docentes + data[i].Docentes;
                acumulador_equipo_entregado=acumulador_equipo_entregado+data[i].Equipo_entregado;
                acumulador_maestros_capacitados=acumulador_maestros_capacitados+data[i].Maestros_capacitados;
                acumulador_promovidos=  acumulador_promovidos+data[i].Maestros_promovidos;
                acumulador_no_promovidos=acumulador_no_promovidos+data[i].Maestros_no_promovidos;
                acumulador_inconclusos=acumulador_inconclusos+data[i].Maestros_desertores;

               $("#escuela").text(Number(i)+1);
               $("#ninos").text(acumulador_ninos_beneficiados);
               $("#equipo").text(acumulador_equipo_entregado);
               $("#capacitados").text(acumulador_maestros_capacitados);
                $(tfoot).find('th').eq(5).html(acumulador_ninos_beneficiados);
                $(tfoot).find('th').eq(6).html(acumulador_docentes);
                $(tfoot).find('th').eq(12).html(acumulador_equipo_entregado);
                $(tfoot).find('th').eq(16).html(acumulador_maestros_capacitados);
                $(tfoot).find('th').eq(17).html(acumulador_promovidos);
                $(tfoot).find('th').eq(18).html(acumulador_no_promovidos);
                $(tfoot).find('th').eq(19).html(acumulador_inconclusos);



                //console.log(nuevo);
              };

            },
        });
        });
        $('#informe-list-form #id_departamento').on('change', function () {
            listar_municipio_departamento('#informe-list-form #id_departamento', '#informe-list-form #id_municipio', true);
        });
  }
}
