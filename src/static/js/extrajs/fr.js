function related(id_empresa, equipo){
    $.ajax({
      url: 'empresa/'+id_empresa+'/',
      dataType: "json",

      success: function(respuesta){
        var texto = "<table class='table table-hover'>";
                        texto += "<thead>";
                          texto += "<tr>";
                            texto += "<td>Id</td>";
                            texto += "<td>Nombre </td>";
                            texto += "<td>Apellido</td>";
                            texto += "<td>Observación</td>";
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