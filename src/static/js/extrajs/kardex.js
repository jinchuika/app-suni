
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
      texto += "<th>id de la salida</th>";
      texto += "<th>Encabezado</th>";
      texto += "<th>Cantidad Egresados</th>";
      texto += "</tr>";
      texto += "</thead>";
      $.each(respuesta.tablainf, function(index, item){
        texto += "<tr><td>" + item.id + "</td><td>"+ item.salida + "</td><td>" + item.cantidad + "</td></tr>";

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


//informe de las Entradas
function get_informe(){
  var ini = $('#ini').val();
  var out = $('#out').val();
  var tipo = $('#tipo select').val();
  $.ajax({
    url: tipo+"/"+ini+'/'+out+"/",
    dataType: "json",
    success: function(respuesta){
      var texto = "<div class='box box-success'><table class='table table-hover table-striped'>";
      texto += "<thead>";
      texto += "<tr>";
      texto += "<th>No. Entrada</th>";
      texto += "<th>Equipo</th>";
      texto += "<th>Fecha</th>";
      texto += "<th>Cantidad</th>";
      if (tipo == 2) {
        texto += "<th>Precio</th>";
        texto += "<th>Factura</th>";
      };
      texto += "</tr>";
      texto += "</thead>";
      if (tipo == 2) {
        $.each(respuesta.tablainf, function(index, itemm){
          texto += "<tr><td>" + itemm.id + "</td><td>"+ itemm.equipo + "</td><td>" + itemm.fecha +"</td><td>" + itemm.cantidad + "</td><td>" + itemm.precio +"</td><td>" + itemm.factura+"</td></tr>";
        })
      } else{
        $.each(respuesta.tablainf, function(index, item){
          texto += "<tr><td>" + item.id + "</td><td>"+ item.equipo + "</td><td>" + item.fecha +"</td><td>" + item.cantidad +"</td></tr>";
        })
        
      };
      document.getElementById('here').innerHTML = texto + "</table></div>";
      

    }
  });
}



