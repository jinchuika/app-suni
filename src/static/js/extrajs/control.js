class Control {
  constructor() {
    var es_numero =function (nota, callback) {
        if (isNaN(nota)) {
            bootbox.alert("No esta permitidos el ingreso de caracteres en esta celda");
            return callback(false)
        }else{
          if(nota>100){
              bootbox.alert("La nota no puede ser mayor de 100 pts");
              return callback(false)
          }else{
            return callback(true)
          }

        }
    }
    var es_letra =function (nota, callback) {
      var var_regex=/[[a-zA-ZñÑüéáíóúÁÉÍÓÚÜ]*\s[a-zA-ZñÑüéáíóúÁÉÍÓÚÜ]*]*/;
        if (var_regex.test(nota)) {
            return callback(true)
        }else{
          bootbox.alert("No esta permitidos el ingreso de numeros o caracteres especiales  en esta celda");
          return callback(false)

        }
    }
    var numero_materias = $('#registro').data("registros");

    for (var k=1;k<numero_materias+1;k++){

      var tabla_equipo = $('#tabla_mas_'+k).DataTable({
          dom: 'lfrtipB',
          buttons: ['excel','pdf','copy']
      });
    }

    var container = document.getElementById('tabla_importar');
    tabla_importar = new Handsontable(container, {
        colWidths: 178,
        colHeaders: ["Nombre","Nota"],
        columns: [
          {data: 'nombre',validator:es_letra},
          {data: 'nota',validator:es_numero},
        ],
        minSpareRows: 1,
        startRows: 1,
        rowHeaders: true,
    });
    $('#btn-crear').on('click', function () {
      $.ajax({
        url:$('#btn-crear').data("url"),
        dataType:'json',
        error:function(){
          console.log("Error");
        },
        success:function(data){
          //console.log(data);
          tabla_importar.loadData(data);
        },
        type: 'GET'
      }
      );
      /*fin ajax*/
    });
    /*redireccionar excel*/
    $('#btn-excel').on('click', function () {
      console.log($('#btn-excel').data("url"));    
      window.open($('#btn-excel').data("url"), '_blank');
    });
    /**/
    /**Guardar informacion**/
    $('#btn-clear').on('click', function () {
        var data_obtenida =[];
      $.each(tabla_importar.getData(), function (index, fila) {
        if(fila[0]!=null && fila[1]!=null){
          var nombre_notas={};
            nombre_notas["nombre"]=fila[0];
            nombre_notas["nota"]=fila[1];
            data_obtenida.push(nombre_notas);
        }


      });
      var data_send=JSON.stringify(data_obtenida)
      $.ajax({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
        },
        url:$('#btn-crear').data("url"),
        dataType:'json',
        data:{datos:data_send,
              materia:$("#id_materia").val(),
              grado:$("#id_grado").val(),
              observacion:$("#id_observacion").val()},
        error:function(){
          console.log("Error");
        },
        success:function(data){
          bootbox.alert({
            message: data,
            className:"modal modal-success fade in",
            callback: function () {
              location.reload(true);
            }
          })

        },
        type: 'POST'
      }
    );
      /*fin ajax*/
    });
  }


}
