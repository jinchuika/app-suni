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
      searching:false,
      paging:true,
      ordering:false,
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
        {data: "activo"},
        {data: "precio"},
        {data: "inventario"},
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
class PrecioEstandarInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  $("[for='id_tipo_dispositivo']").css({"visibility":"hidden"});
  $("#id_tipo_dispositivo").css({"visibility":"hidden"});
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
      searching:false,
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
        {data: "id_dispositivo"},
        {data: "precio"},
        {data: "inventario"}
      ]
    });
    tablaPrecio.clear().draw();
    tablaPrecio.ajax.reload();
  });
  }
}
class ExistenciaInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({    
      footerCallback: function( tfoot, data, start, end, display){
          for (var i in data){
            $(tfoot).find('th').eq(3).html( "Total : "+ parseFloat(data[i].acumulador_anterior).toLocaleString());
            $(tfoot).find('th').eq(5).html( "Total : "+ parseFloat(data[i].acumulador_total ).toLocaleString());
          };
        },
      searching:false,
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
        {data: "tipo"},
        {data: "cantidad"},
        {data: "precio_anterior", render: function(data, type, full, meta){
          return parseFloat(full.precio_anterior).toLocaleString('en');
        }},
        {data: "total_anterior", render: function(data, type, full, meta){
          return parseFloat(full.total_anterior).toLocaleString('en');
        }},
        {data: "precio", render: function(data, type, full, meta){
          return parseFloat(full.precio).toLocaleString('en');
        }},
        {data: "total", render:function(data, type, full, meta){
          return parseFloat(full.total).toLocaleString('en');
        }},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}
class EntradaInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
    headerCallback:function (thead, data, start, end, display ){
      for(var i in data){
        $(thead).find('th').eq(0).html( "Tipo dispositivo:" + data[i].tipo_dispositivo );
        $(thead).find('th').eq(1).html( "Fecha:" + data[i].rango_fechas);
        $(thead).find('th').eq(2).html( "Saldo inicial cantidad:"+ data[i].total_final );
        $(thead).find('th').eq(3).html( "Saldo inicial dinero:" + data[i].total_costo );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "Saldo Final Cantidad : "+ data[i].total_despues );
          $(tfoot).find('th').eq(1).html( "Saldo Final Dinero : "+ data[i].total_costo_despues );
        };
      },
      searching:false,
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
        {data: "fecha"},
        {data: "id"},
        {data: "util"},
        {data: "precio"},
        {data: "total"},
        {data: "tipo"},
        {data: "proveedor"},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}
