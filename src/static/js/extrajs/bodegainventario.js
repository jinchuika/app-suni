class ResumenBodegaPrint{
  constructor(){
   var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var fecha_min = urlParams.get('fecha_min');
    var fecha_max = urlParams.get('fecha_max');
    const Meses = ["ENERO", "FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    var getLongMonthName = function(date) {
    return Meses[date.getMonth() +1 ];
    }
    const fecha = new Date(fecha_min);    
    document.getElementById("rango").innerHTML = fecha_min +"  AL "+ fecha_max
    document.getElementById("fecha").innerHTML =  "  RESUMEN DE INVENTARIO " +getLongMonthName(new Date(fecha_min)) +"  " +fecha.getFullYear();
    /*CONSUMIR API*/
    var urldispositivo = $("#tabla").data("url")
    var cuerpoTabla = $("#tabla tbody")
    $.ajax({
      type: 'GET',
      url: urldispositivo,
      dataType: 'json',
      data: {
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        fecha_min: fecha_min,
        fecha_max: fecha_max

      },
      success: function (response) {
        response.forEach(function(resultRow){
          var tableRow = "<tr style='height: 60px;'>" +"<td> <h4>"+resultRow.tipo+"</h4></td>"+"<td><h4>"+resultRow.existencia_anterior+"</h4></td>"+"<td><h4>"+resultRow.entradas+"</h4></td>"+"<td><h4>"+resultRow.salidas+"</h4></td>"+"<td><h4>"+resultRow.existencia+"</h4></td>"+"<td id='borde1'>"+""+"</td>"+"</tr>";
          cuerpoTabla.append(tableRow);

        });
        document.getElementById("spinner").style.display='none';
      },
      error: function (response) {

      }
    });
    /*FIN DE CONSUMO*/


  }
}
