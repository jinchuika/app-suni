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
        {data: "inventario", render: function(data, type, full, meta){
          if(full.inventario == 'dispositivo'){
               return "<span class='label label-primary'>Dispositivo</span>";
             }else{
               return "<span class='label label-danger'>Repuesto</span>";
             }
        }},
        {data: "activo", render: function(data, type, full, meta){
          if(full.activo == true){
               return "<input type='checkbox' class='icheckbox_flat-green' name='activo' disabled checked />";
             }else{
               return "<input type='checkbox' class='icheckbox_flat-green' name='activo' disabled />";;
             }
        }},
        {data: "creado_por"},
        {data: "activo", render: function(data, type, full, meta){
             if(full.revaluar == false && full.activo == true){
              return "<a id='revaluar-precio' data-id="+full.id+"  class='btn btn-info btn-revaluar'>Revaluar</a>";
             }else{
               return "<span class='label label-success'>Revaluado</span>";
             }
        }}
      ],
    });
    tablaPrecio.clear().draw();
    tablaPrecio.ajax.reload();
    var tablaPreciobody = $('#precioestandar-table tbody');
    tablaPreciobody.on('click', '.btn-revaluar',function (){
      let data_fila= tablaPrecio.row($(this).parents('tr')).data();
      $.ajax({
            type: 'POST',
            url: urlPrecio+"reevaluar/",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                id:data_fila.id
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
        $(thead).find('th').eq(0).html( data[i].tipo_dispositivo );
        $(thead).find('th').eq(1).html( data[i].rango_fechas);
        $(thead).find('th').eq(2).html( "EXISTENCIA INICIAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
        $(thead).find('th').eq(3).html( "SALDO INICIAL: " + parseFloat(data[i].total_costo).toLocaleString('en') );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
          $(tfoot).find('th').eq(1).html( "SALDO FINAL: "+ parseFloat(data[i].total_costo_despues).toLocaleString('en') );
        };
      },
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:false,
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
        {data: "id", render: function(data, type, full, meta){
          return "<a href="+full.url+">"+full.id+"</a>";
        }},
        {data: "util"},
        {data: "precio", render: function(data, type, full, meta){
          return parseFloat(full.precio).toLocaleString('en');
        }},
        {data: "total", render: function(data, type, full, meta){
          return parseFloat(full.total).toLocaleString('en');
        }},
        {data: "tipo"},
        {data: "proveedor"},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}

class EntradaDispositivoInforme {
  constructor() {
  let precioestandar_informe = $("#entradadispositivo-list-form");
  var urlPrecio= $('#entrada-dispositivo-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#entrada-dispositivo-table').DataTable({
    headerCallback:function (thead, data, start, end, display ){
      for(var i in data){
        $(thead).find('th').eq(0).html( data[i].tipo_dispositivo );
        $(thead).find('th').eq(1).html( data[i].rango_fechas);
        $(thead).find('th').eq(2).html( "EXISTENCIA INICIAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
        };
      },
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:false,
      ordering:true,
      processing:true,
      destroy:true,
      ajax:{
        url:urlPrecio,
        dataSrc:'',
        cache:false,
        processing:true,
        data: function () {
          return $('#entradadispositivo-list-form').serializeObject(true);
        }
      },
      columns: [
        {data: "triage", render: function(data, type, full, meta){
          return "<a href="+full.url+">"+full.triage+"</a>";
        }},
        {data: "entrada", render: function(data, type, full, meta){
          return "<a href="+full.url_entrada+">"+full.entrada+"</a>";
        }},
        {data: "fecha"},
        {data: "tipo_entrada"},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}
class SalidaInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
    headerCallback:function (thead, data, start, end, display ){
      for(var i in data){
        $(thead).find('th').eq(0).html( data[i].tipo_dispositivo );
        $(thead).find('th').eq(1).html( data[i].rango_fechas);
        $(thead).find('th').eq(2).html( "EXISTENCIA INICIAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
        $(thead).find('th').eq(3).html( "SALDO INICIAL: " + parseFloat(data[i].total_costo).toLocaleString('en') );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
          $(tfoot).find('th').eq(1).html( "SALDO FINAL: "+ parseFloat(data[i].total_costo_despues).toLocaleString('en') );
        };
      },
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:false,
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
        {data: "id", render: function(data, type, full, meta){
          return "<a href="+full.url+">"+full.no_salida+"</a>";
        }},
        {data: "util"},
        {data: "precio", render: function(data, type, full, meta){
          return parseFloat(full.precio).toLocaleString('en');
        }},
        {data: "total", render: function(data, type, full, meta){
          return parseFloat(full.total).toLocaleString('en');
        }},
        {data: "tipo"},
        {data: "beneficiado"},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}


class DesechoInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
    headerCallback:function (thead, data, start, end, display ){
      for(var i in data){
        $(thead).find('th').eq(0).html( data[i].tipo_dispositivo );
        $(thead).find('th').eq(1).html( data[i].rango_fechas);
        $(thead).find('th').eq(2).html( "EXISTENCIA INICIAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
        $(thead).find('th').eq(3).html( "SALDO INICIAL: " + parseFloat(data[i].total_costo).toLocaleString('en') );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
          $(tfoot).find('th').eq(1).html( "SALDO FINAL: "+ parseFloat(data[i].total_costo_despues).toLocaleString('en') );
        };
      },
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:false,
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
        {data: "id", render: function(data, type, full, meta){
          return "<a href="+full.url+">"+full.id+"</a>";
        }},
        {data: "util"},
        {data: "precio", render: function(data, type, full, meta){
          return parseFloat(full.precio).toLocaleString('en');
        }},
        {data: "total", render: function(data, type, full, meta){
          return parseFloat(full.total).toLocaleString('en');
        }},
        {data: "recolectora"},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}

class ResumenInforme {
  constructor() {
  let precioestandar_informe = $("#precioestandar-list-form");
  var urlPrecio= $('#precioestandar-table').data("api");
  precioestandar_informe.submit(function (e){
    e.preventDefault();
    var tablaPrecio = $('#precioestandar-table').DataTable({
    headerCallback:function (thead, data, start, end, display ){
      for(var i in data){
        $(thead).find('th').eq(0).html( data[i].rango_fechas);
        $(thead).find('th').eq(1).html( "EXISTENCIA INICIAL: "+ parseFloat(data[i].total_inicial).toLocaleString('en') );
        $(thead).find('th').eq(2).html( "SALDO INICIAL: " + parseFloat(data[i].costo_inicial).toLocaleString('en') );
      };

    },
    footerCallback: function( tfoot, data, start, end, display){
        for (var i in data){
          $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
          $(tfoot).find('th').eq(1).html( "SALDO FINAL: "+ parseFloat(data[i].costo_final).toLocaleString('en') );
        };
      },
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:false,
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
        {data: "existencia_anterior", render: function(data, type, full, meta){
          return parseFloat(full.existencia_anterior).toLocaleString('en');
        }},
        {data: "saldo_anterior", render: function(data, type, full, meta){
          return parseFloat(full.saldo_anterior).toLocaleString('en');
        }},
        {data: "entradas", render: function(data, type, full, meta){
          return parseFloat(full.entradas).toLocaleString('en');
        }},
        {data: "salidas", render: function(data, type, full, meta){
          return parseFloat(full.salidas).toLocaleString('en');
        }},
        {data: "existencia", render: function(data, type, full, meta){
          return parseFloat(full.existencia).toLocaleString('en');
        }},
        {data: "saldo_actual", render: function(data, type, full, meta){
          return parseFloat(full.saldo_actual).toLocaleString('en');
        }},
      ]
    });
    tablaPrecio.clear().draw();
    //tablaPrecio.ajax.reload();
  });
  }
}