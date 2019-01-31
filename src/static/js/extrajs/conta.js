class PeriodoFiscal {
  constructor() {
    let asignar_periodo = $('#periodo-fiscal-form');
    asignar_periodo.submit(function (e){
      e.preventDefault();
      $.ajax({
      type: "POST",
      url: asignar_periodo.attr('action'),
      data:asignar_periodo.serialize(),
      success: function (response){
        bootbox.alert("Asignacion correctamente");

      },
      error:function(jqXHR, textStatus, errorThrown){
        bootbox.alert(jqXHR.responseText);
      }
    });
    });

  }
}
class PrecioEstandar {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
      searching:true,
      paging:true,
      ordering:true,
      processing:true,
      destroy:true,
      ajax:{
        url:urlPrecio,
        dataSrc:'',
        cache:false,
        processing:true,
        data: function () {
          return $('#precioestandar-list-form').serializeObject(true);
        }
      },
      columns: [
        {data: "id"},
        {data: "periodo"},
        {data: "id_dispositivo"},  
        {data: "precio"},
        {data: "inventario"},
        {data: "activo", render: function(data, type, full, meta){
          if(full.activo == true){
               return "<input type='checkbox' name='activo' disabled checked />";
             }else{
               return "<input type='checkbox' name='activo' disabled />";;
             }
        }},
        {data: "creado_por"},
        {data: "activo", render: function(data, type, full, meta){
             if(full.activo == true){
               return "<button id='buttonrevaluar'"+"data-tipo='"+full.tipo_dispositivo+"'class='btn btn-info btn-revaluar'>Reevaluar</button>";
             }else{
               return "";
             }
        }}
      ]

    });
    tablaPrecio.clear().draw();
    tablaPrecio.ajax.reload();
    var tablaPreciobody = $('#precioestandar-table tbody');
    tablaPreciobody.on('click', '.btn-revaluar',function (){
      let tipo= tablaPrecio.row($(this).parents('tr')).data();
      $.ajax({
            type: 'POST',
            url: urlPrecio+"reevaluar/",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                tipo_dispositivo:tipo.tipo_dispositivo
            },
            success: function (response) {
              bootbox.alert("Reevaluacion completa");
              console.log("Reevaluacion completa");
            },
        });

    });
  });



  }
}
