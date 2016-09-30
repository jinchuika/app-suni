
//para entrada
function entrada(id_equipo, equipo){
    $.ajax({
      url: 'entrada/'+id_equipo+'/',
      dataType: "json",

      success: function(respuesta){
        var texto = "<table class='table table-datatables'>";
                        texto += "<thead>";
                          texto += "<tr>";
                            texto += "<td>Id de entrada</td>";
                            texto += "<td>Fecha </td>";
                            texto += "<td>Cantidad Ingresado</td>";
                            texto += "<td>Observación</td>";
                            texto += "<td>Usuario</td>";
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


//para salida
function salida(id_equipo, equipo){
    $.ajax({
      url: 'salida/'+id_equipo+'/',
      dataType: "json",

      success: function(respuesta){
        var texto = "<table class='table table-datatables'>";
                        texto += "<thead>";
                          texto += "<tr>";
                            texto += "<td>id de entrada</td>";
                            texto += "<td>Fecha </td>";
                            texto += "<td>Cantidad Ingresado</td>";
                            texto += "<td>observación</td>";
                          texto += "</tr>";
                        texto += "</thead>";
        $.each(respuesta.tablainf, function(index, item){
          texto += "<tr><td>" + item.id + "</td><td>"+ item.fecha + "</td><td>" + item.cantidad + "</td><td>" + item.observacion +"</td></tr>";
          
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


