
//para entrada
function entrada(id_equipo, equipo){
  $.ajax({
    url: 'entrada/'+id_equipo+'/',
    dataType: "json",

    success: function(respuesta){
      var texto = "<table class='table table-datatables'>";
      texto += "<thead>";
      texto += "<tr>";
      texto += "<th>Id de entrada</th>";
      texto += "<th>Fecha </th>";
      texto += "<th>Cantidad Ingresado</th>";
      texto += "<th>Observación</th>";
      texto += "</tr>";
      texto += "</thead>";
      $.each(respuesta.tablainf, function(index, item){
        texto += "<tr><td>" + item.id + "</td><td>"+ item.fecha + "</td><td>" + item.cantidad + "</td><td>" + item.observacion + "</td></tr>";

      })

      bootbox.alert({
        title: "Id del equipo: " + id_equipo + "<br><br> Nombre del equipo:  " + equipo,
        message: texto +  "</table>",
        size : 'large',
        backdrop: true
      });


    }
  });
}


//para salida
function salida(id_equipo, equipo){
  $.ajax({
    url: 'salida/'+id_equipo+'/',
    dataType: "json",

    success: function(respuesta){
      var texto = "<table class='table table-datatables'>";
      texto += "<thead>";
      texto += "<tr>";
      texto += "<th>id de entrada</th>";
      texto += "<th>Fecha </th>";
      texto += "<th>Cantidad Egresados</th>";
      texto += "<th>observación</th>";
      texto += "<th>Usuario</th>";
      texto += "</tr>";
      texto += "</thead>";
      $.each(respuesta.tablainf, function(index, item){
        texto += "<tr><td>" + item.id + "</td><td>"+ item.fecha + "</td><td>" + item.cantidad + "</td><td>" + item.observacion + "</td><td>" + item.tecnico + "</td></tr>";

      })

      bootbox.alert({
        title: "Id del equipo: " + id_equipo + "<br><br> Nombre del equipo:  " + equipo,
        message: texto +  "</table>",
        size : 'large',
        backdrop: true
      });


    }
  });
}




//para informe
function informe(){
 var ini = $('#ini').val();
 var out = $('#out').val();
 $(location).attr('href', 'informe/'+ini+"/"+out+"/");
}



