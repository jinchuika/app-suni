(function( ProveedorList, $, undefined ) {
    ProveedorList.init = function () {
        $('#proveedor-tabla').DataTable();
        $('.btn-proveedor').click(function () {
            $.ajax({
                url: $('#proveedor-tabla').data('url-entrada'),
                data: {
                    proveedor: $(this).data('id')
                }
            })
        })
    }
}( window.ProveedorList = window.ProveedorList || {}, jQuery ));


(function( EntradaCreate, $, undefined ) {
    var generar_tabla_entrada = function (entrada) {
        var tabla_html = '<table class="table table-striped" id="tabla-entrada">';
        tabla_html += '<tr><th>Número:</th><td>' + entrada.id +'</td></tr>';
        tabla_html += '<tr><th>Artículo:</th><td>' + entrada.equipo +'</td></tr>';
        tabla_html += '<tr><th>Cantidad:</th><td>' + entrada.cantidad +'</td></tr>';
        tabla_html += '<tr><th>Fecha:</th><td>' + entrada.fecha +'</td></tr>';
        tabla_html += '<tr><th>Proveedor:</th><td>' + entrada.proveedor +'</td></tr>';
        tabla_html += '<tr><th>Estado:</th><td>' + entrada.estado +'</td></tr>';
        tabla_html += '<tr><th>Tipo de entrada:</th><td>' + entrada.tipo +'</td></tr>';
        if (entrada.factura) {
            tabla_html += '<tr><th>No. Factura:</th><td>' + entrada.factura +'</td></tr>';
        }
        if (entrada.precio) {
            tabla_html += '<tr><th>Precio:</th><td>' + entrada.precio +'</td></tr>';
        }
        tabla_html += '<tr><th>Observaciones:</th><td>' + entrada.observacion +'</td></tr>';
        tabla_html += '</table>';

        var tabla_pdf = {
            table: {
                widths: [100, 200],
                body: [
                    ['Número:', entrada.id],
                    ['Artículo', entrada.equipo],
                    ['Cantidad', entrada.cantidad],
                    ['Fecha', entrada.fecha],
                    ['Proveedor', entrada.proveedor],
                    ['Estado', entrada.estado],
                    ['Tipo de entrada', entrada.tipo],
                    ['No. factura', entrada.factura],
                    ['Precio', entrada.precio],
                    ['Observaciones', entrada.observacion],
                ]
            }
        }

        return {html: tabla_html, pdf: tabla_pdf};
    }
    EntradaCreate.init = function () {
        $('#entrada-buscar-form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                url: $(this).prop('action'),
                data: $(this).serializeObject(),
                success: function (respuesta) {
                    if (respuesta.length == 1) {
                        var tabla = generar_tabla_entrada(respuesta[0]);

                        bootbox.dialog({
                            title: 'Entrada ' + respuesta[0].id,
                            message: tabla.html,
                            buttons: {
                                imprimir: {
                                    label: 'Imprimir',
                                    className: 'btn-info',
                                    callback: function () {
                                        var contenido = {
                                            content: [
                                                {text: 'Entrada no. '+respuesta[0].id, style: 'header'},
                                                tabla.pdf
                                                ],
                                                styles: {
                                                    header: {
                                                        fontSize: 18,
                                                        bold: true,
                                                        margin: [0, 0, 0, 10]
                                                    }
                                                },
                                        };
                                        pdfMake.createPdf(contenido).download('Entrada.pdf');
                                    }
                                },
                                cerrar: {
                                    label: 'Cerrar',
                                    className: 'btn-danger',
                                    callback: function () {
                                        // body...
                                    }
                                }
                            }
                        })
                    }
                }
            })
        })
    }
}( window.EntradaCreate = window.EntradaCreate || {}, jQuery ));

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
      texto += "<th>No. de salida</th>";
      texto += "<th>Técnico</th>";
      texto += "<th>Fecha</th>";
      texto += "<th>Cantidad Egresados</th>";
      texto += "</tr>";
      texto += "</thead>";
      $.each(respuesta.tablainf, function(index, item){
        texto += "<tr><td>" + item.id + "</td><td>"+ item.tecnico + "</td><td>" +item.fecha + "</td><td>" + item.cantidad + "</td></tr>";

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
  if (ini == "") {
    ini = "all";
};
if (out == "") {
    out = "all";
};
$.ajax({
    url: "informe/"+ ini + "/" + out + "/",
    dataType: "json",
    success: function(respuesta){
      var texto = "";
      if (respuesta.properties.length == 0){
        texto += "<div class='box box-danger'><div class='box-body'>";
        texto += "<h4 align='center'>No se encontraron resultados</h4></div></div>";
    } else{
        texto += "<div class='box box-success'><table class='table table-hover table-striped table-bordered'>";
        texto += "<thead>";
        texto += "<tr>";
        texto += "<th>Nombre</th>";
        texto += "<th>No. Entradas</th>";
        texto += "<th>No. Salidas</th>";
        texto += "<th>Cant. Ingresada</th>";
        texto += "<th>Cant. Egresadas</th>";
        texto += "<th>Diferencia</th>";
        texto += "<th>Existencia actual</th>";
        texto += "</tr>";
        texto += "</thead>";
        $.each(respuesta.properties, function(index, item){
          texto += "<tr><td>"+item.nombre+"</td><td>"+item.cantidad_ingresos+"</td><td>"+item.cantidad_egresos+"</td><td>";
          texto += item.ingreso+"</td><td>"+item.egreso+"</td><td>"+item.diferencia+"</td><td>"+item.existencia_actual+"</td></tr>";
      })
        texto += "</table></div>"
    };
    document.getElementById('info').innerHTML = texto;
}
});
}


//informe de las Entradas
function get_informe_entradas(){
  var ini = $('#ini').val();
  var out = $('#out').val();
  var proveedor = $('#field #id_proveedor').val();
  var tipo = $('#field #id_tipo_entrada').val();
  if (proveedor < 1) {
    proveedor = "all";
};
if (tipo < 1 ) {
    tipo = "all";
};
if (ini == "") {
    ini = "all";
};
if (out == "") {
    out = "all";
};
$.ajax({
    url: proveedor+"/"+tipo+"/"+ini+"/"+out+"/",
    dataType: "json",
    success: function(respuesta){
      var texto = "";
      if (respuesta.tablainf.length == 0 ) {
        texto += "<div class='box box-danger'><div class='box-body'>";
        texto += "<h4 align='center'> No se encontraron resultados </h4></div></div>";
    } else{
        texto = "<div class='box box-success'><table class='table table-hover table-striped'>";
        texto += "<thead>";
        texto += "<tr>";
        texto += "<th>No. Entrada</th>";
        texto += "<th>Tipo</th>"
        texto += "<th>Proveedor</th>"
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
            texto += "<tr><td>" + itemm.id + "</td><td>" + itemm.tipo + "</td><td>"+ itemm.prov +"</td><td>"+ itemm.equipo + "</td><td>" + itemm.fecha +"</td><td>" + itemm.cantidad + "</td><td>Q " + itemm.precio +"</td><td>" + itemm.factura+"</td></tr>";
        })
      } else{
          $.each(respuesta.tablainf, function(index, item){
            texto += "<tr><td>" + item.id + "</td><td>"+ item.tipo +"</td><td>"+ item.prov +"</td><td>"+ item.equipo + "</td><td>" + item.fecha +"</td><td>" + item.cantidad +"</td></tr>";
        })
          texto += "</table></div>";
      };
  };
  document.getElementById('here').innerHTML = texto;
}
});
}

//informe de las Entradas
function get_salidas(){
  var ini = $('#ini').val();
  var out = $('#out').val();
  var tecnico = $('#tecnico select').val();
  if (tecnico < 1) {
    tecnico = "all"
};
if (ini == "") {
    ini = "all";
};
if (out =="") {
    out = "all";
};
$.ajax({
    url: tecnico+"/"+ini+'/'+out+"/",
    dataType: "json",
    success: function(respuesta){
      if (respuesta.tablainf.length == 0) {
        var texto = "<div class='box box-danger'><div class='box-body'>"
        texto += " <h4 align='center'> No se encontraron resultados <h4></div> </div>"
    } else{
        var texto = "<div class='box box-success'><table class='table table-hover table-striped'>";
        texto += "<thead>";
        texto += "<tr>";
        texto += "<th>No. Salida</th>";
        texto += "<th>Técnico</th>";
        texto += "<th>Fecha</th>";
        texto += "<th>Equipo</th>";
        texto += "<th>Cantidad</th>";
        texto += "</tr>";
        texto += "</thead>";
        $.each(respuesta.tablainf, function(index, item){
          texto += "<tr><td>" + item.id + "</td><td>"+ item.tecnico + "</td><td>"+ item.fecha + "</td><td>" + item.equipo +"</td><td>" + item.cantidad +"</td></tr>";
      })
        texto += "</table></div>";
    };
    document.getElementById('informe').innerHTML = texto;


}
});
}


