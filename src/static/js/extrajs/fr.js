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


function contacto(id_tag, tag){
    $.ajax({
      url: 'empresa/'+id_tag+'/',
      dataType: "json",

      success: function(respuesta){
        var texto = "<table class='table table-hover'>";
                        texto += "<thead>";
                          texto += "<tr>";
                            texto += "<th>Nombre</th>";
                            texto += "<th>Empresa </th>";
                            texto += "<th>Puesto</th>";
                            texto += "<th>Teléfono</th>";
                            texto += "<th>Correo</th>";
                          texto += "</tr>";
                        texto += "</thead>";
        $.each(respuesta.contacto, function(index, item){
          texto += "<tr><td>" + item.nombre + "</td><td>"+ item.empresa + "</td><td>" + item.puesto + "</td><td>" + item.telefono + "</td><td>" + item.correo + "</td></tr>";
          
        })
        
          bootbox.alert({
            title: "Id del tag: " + id_tag + "<br><br> Etiqueta:  " + tag,
            message: texto +  "</table>",
            size : 'large',
            backdrop: true
           });

        
      }
    });
  }