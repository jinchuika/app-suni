(function( CourseraDashboard, $, undefined ) {

}( window.CourseraDashboard = window.CourseraDashboard || {}, jQuery ));
class CourseraInforme {
  constructor() {
    var tablaPrecio = $('#coursera-table-search').DataTable({
      searching:true,
      paging:true,
      ordering:true,
      processing:true,
      destroy:true,
      ajax:{
        type: 'GET',
        url: $('#coursera-table-search').data("url"),
        dataSrc:'',
        cache:false,
        processing:true,
        },
      columns: [
        {data: "aliado"},
        {data: "miembros"},
        {data: "invitaciones"},
        {data: "inscritos"},
        {data: "aceptacion"},
        {data: "graduados"}
      ],
      footerCallback: function( tfoot, data, start, end, display){
          var api = this.api();
          for (var i in data){
            $(tfoot).find('th').eq(1).html( data[0].total_miembros);
            $(tfoot).find('th').eq(2).html( data[0].total_invitaciones);
            $(tfoot).find('th').eq(3).html( data[0].total_inscrito);
            $(tfoot).find('th').eq(4).html( data[0].total_aceptacion.toFixed(2));
            $(tfoot).find('th').eq(5).html( data[0].total_graduados);
          };
        },
    });
  }
}
class CourseraGenerarInforme {
  constructor() {
    $('#generar-graficas').click(function(){
      $.ajax({
        url:$('#generar-graficas').data("url"),
        dataType:'json',
        error:function(){
          console.log("Error");
        },
        success:function(data){
          bootbox.alert(data, function(){
                location.href = '/coursera/informe/excel/';
          });

        },
        type: 'GET'
      }
      );
      /*fin ajax*/
    });
  }
}
