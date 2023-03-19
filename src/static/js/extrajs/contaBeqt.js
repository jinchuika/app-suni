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
          var api = this.api();
          for (var i in data){
            $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
            $(tfoot).find('th').eq(1).html( "CANTIDAD TOTAL: "+ parseFloat(api.column(2, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(2).html( "TOTAL: "+ parseFloat(api.column(4, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(3).html( "SALDO FINAL: "+ parseFloat(data[i].total_costo_despues).toLocaleString('en') );
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
        order: [[ 3, "desc" ]],
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
            console.log(full)
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
          var api = this.api();
          for (var i in data){
            $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_despues).toLocaleString('en') );
            $(tfoot).find('th').eq(1).html( "CANTIDAD TOTAL: "+ parseFloat(api.column(2, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(2).html( "TOTAL: "+ parseFloat(api.column(4, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(3).html( "SALDO FINAL: "+ parseFloat(data[i].total_costo_despues).toLocaleString('en') );
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
        var api = this.api();
          for (var i in data){
            $(tfoot).find('th').eq(0).html( "EXISTENCIA FINAL: "+ parseFloat(data[i].total_final).toLocaleString('en') );
            $(tfoot).find('th').eq(1).html( "ENTRADAS: "+ parseFloat(api.column(3, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(2).html( "SALIDAS: "+ parseFloat(api.column(4, {page: 'current'}).data().sum() ).toLocaleString('en'));
            $(tfoot).find('th').eq(3).html( "SALDO FINAL: "+ parseFloat(data[i].costo_final).toLocaleString('en') );
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