(function (AlertaEnCreacion, $, undefined) {
    AlertaEnCreacion.init = function () {
        var mensaje = document.getElementById("id_en_creacion");
        var urldispositivo = $("#entrada-detalle-form").data("api");
        var primary_key = $("#entrada-detalle-form").data("key");
        $('#id_en_creacion').click(function () {
            if ($("#id_en_creacion").is(':checked')) {
                bootbox.alert("esta activado");
            } else {
                bootbox.confirm({
                            message: "Esta Seguro que quiere Terminar la Creacion de la Entrada",
                            buttons: {
                                confirm: {
                                    label: 'Si',
                                    className: 'btn-success'
                                },
                                cancel: {
                                    label: 'No',
                                    className: 'btn-danger'
                                }
                            },
                            callback: function (result) {
                                if(result == true){
                                  /**/
                                  $.ajax({
                                      type: 'POST',
                                      url: urldispositivo,
                                      dataType: 'json',
                                      data: {
                                          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                          primary_key :primary_key
                                      },
                                      success: function (response) {
                                          bootbox.alert("Entrada Cuadrada");
                                      },
                                      error: function (response) {
                                           var jsonResponse = JSON.parse(response.responseText);
                                           bootbox.alert(jsonResponse["mensaje"]);
                                      }
                                  });
                                  /**/

                                }
                            }
                          });
            }
        });


    }

}(window.AlertaEnCreacion = window.AlertaEnCreacion || {}, jQuery));

class EntradaCreate {
  constructor() {
    $("[for='id_factura']").css({"visibility":"hidden"});
    $("#id_factura").css({"visibility":"hidden"});

    $('#id_tipo').change( function() {
      var selected_tipo = $('#id_tipo option:selected').text();
      if(selected_tipo == 'Compra'){
        $("[for='id_factura']").css({"visibility":"visible"});
        $("#id_factura").css({"visibility":"visible"});
      } else {
        $("[for='id_factura']").css({"visibility":"hidden"});
        $("#id_factura").css({"visibility":"hidden"});
      }
    });
  }
}

class EntradaUpdate {
    constructor() {
        let entrada_table = $('#entrada-table');
        var url_qr = $('#entrada-detalle-form').data("apiqr");
        this.api_url = entrada_table.data("api");
        this.pk = entrada_table.data("pk");
        this.url_filtrada = this.api_url + "?asignacion=" + this.pk;
        var key = entrada_table.data("pk");
        $("[for='id_proveedor_kardex']").css({"visibility":"hidden"});
        $('#id_proveedor_kardex').next(".select2-container").hide();
        $("[for='id_estado_kardex']").css({"visibility":"hidden"});
        $('#id_estado_kardex').next(".select2-container").hide();
        $("[for='id_tipo_entrada_kardex']").css({"visibility":"hidden"});
        $('#id_tipo_entrada_kardex').next(".select2-container").hide();

        $('#id_tipo_dispositivo').change( function() {
          $('#id_descripcion').val($('#id_tipo_dispositivo option:selected').text());
          let urldispositivo = tabla_temp.api_url + key + "/validar_kardex/";
          let tipo_dispositivo=$('#id_tipo_dispositivo option:selected').val();
          EntradaUpdate.validar_kardex(urldispositivo, tipo_dispositivo);
        });

        this.tabla = entrada_table.DataTable({
            dom: 'Bfrtip',
            buttons: ['excel', 'pdf', 'copy'],
            paging: false,
            searching:true,
            ordering: true,
            processing: true,
            ajax: {
                url: this.url_filtrada,
                dataSrc: '',
                cache: true,
                data: this.api_url
            },
            columns: [
                {data: "tdispositivo"},
                {data:"descripcion"},
                {data: "util"},
                {data: "repuesto"},
                {data: "desecho"},
                {data: "total"},
                {data: "precio_unitario"},
                {data: "precio_subtotal"},
                {data: "precio_descontado"},
                {data: "precio_total"},
                {data: "creado_por"},
                {
                    data: "",render: function(data, type, full, meta){
                      if(full.dispositivos_creados == true || full.repuestos_creados == true ){
                          if(full.usa_triage == "False"){
                            if(full.ingresado_kardex == true){
                              return "";
                            }else{
                              return "<a href="+full.update_url+" class='btn btn-info btn-editar'>Editar</a>";
                            }
                          }else{
                              return "";
                          }
                      }else{
                        return "<a href="+full.update_url+" class='btn btn-info btn-editar'>Editar</a>";
                      }
                    }
                },
                {
                    data: "", render: function(data, type, full, meta){
                      if(full.tipo_entrada != "Especial"){
                          if(full.dispositivos_creados == false){
                            if(full.usa_triage == "True" && full.util >= 1){
                              return "<button class='btn btn-primary btn-dispositivo'>Crear Disp</button>";
                            }else{
                              return "";
                            }
                          }else{
                             if(full.enviar_kardex == true){
                               if(full.ingresado_kardex == true){
                                 return "<a target='_blank' rel='noopener noreferrer' href="+full.url_kardex+" class='btn btn-success btn-ulrKardex'>Detalle</a>";
                               }else{
                                 if(full.util > 0){
                                  return "<a target='_blank' rel='noopener noreferrer' class='btn btn-success btn-kardex'>Agregar a kardex</a>";
                                }else{
                                  return "";
                                }

                               }

                             }else{

                             }
                              if(full.qr_dispositivo == true){
                                if(full.usa_triage == "True"){
                                    return "<a target='_blank' rel='noopener noreferrer' href="+full.dispositivo_list+" class='btn btn-success'>Listado Dispositivo</a>";
                                }else{
                                  return " ";
                                }

                              }else{
                                if(full.usa_triage == "True"){
                                    return "<a target='_blank' rel='noopener noreferrer' href="+full.dispositivo_qr+" class='btn btn-primary btn-Qrdispositivo'>QR Dispositivo</a>";
                                }else {
                                  return " ";
                                }
                            }
                          }
                      }else{
                        return "";
                      }

                    }
                },
                {
                    data: "", render: function(data, type, full, meta){
                      if(full.tipo_entrada != "Especial"){
                        if(full.repuestos_creados == false){
                          if(full.usa_triage == "True" && full.repuesto > 0){
                              return "<button class='btn btn-warning btn-repuesto'>Crear Rep</button>";
                          }else{
                            return " ";
                          }
                        }else{
                          if(full.qr_repuestos == true){
                            if(full.usa_triage=="True"){
                                  return "<a target='_blank' rel='noopener noreferrer' href="+full.repuesto_list+" class='btn btn-success'>Listado Repuestos</a>";
                            }else{
                              return " ";
                            }
                          }else{
                            if(full.usa_triage=="True"){
                                return "<a target='_blank' rel='noopener noreferrer' href="+full.repuesto_qr+" class='btn btn-primary btn-Qrepuesto'>QR Repuestos</a>";
                            }else{
                              return " ";
                            }
                          }
                        }
                      }else{
                        return "";
                      }
                    }
                },
            ]
        });

        let tablabody = $('#entrada-table tbody');
        let tabla_temp = this;

        tablabody.on('click', '.btn-editar', function () {
            let data_fila = this.tabla.row($(this).parents('tr')).data();
            location.href = data_fila.update_url;
        });

        tablabody.on('click', '.btn-Qrdispositivo', function () {
          let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
        $.ajax({
              type: "POST",
              url: url_qr,
              dataType: 'json',
              data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                detalles_id:data_fila.id,
                tipo:"dispositivo"
              },
              success: function (response) {
                   location.reload();
              },
          });

        });

        tablabody.on('click', '.btn-Qrepuesto', function () {
          let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
        $.ajax({
              type: "POST",
              url: url_qr,
              dataType: 'json',
              data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                detalles_id:data_fila.id,
                tipo:"repuestos"
              },
              success: function (response) {
                 location.reload();
              },
          });

        });

        tablabody.on('click', '.btn-dispositivo', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            bootbox.confirm({
                        message: "Esta seguro que desea crear estos dispositivos",
                        buttons: {
                            confirm: {
                                label: 'Si',
                                className: 'btn-success'
                            },
                            cancel: {
                                label: 'No',
                                className: 'btn-danger'
                            }
                        },
                        callback: function (result) {
                            if(result == true){
                              /**/

                                let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_dispositivos/";
                                EntradaUpdate.crear_dispositivos(urldispositivo);
                            }
                        }
                      });


        });

        tablabody.on('click', '.btn-repuesto', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
          bootbox.confirm({
                      message: "Esta seguro que desea crear estos repuestos",
                      buttons: {
                          confirm: {
                              label: 'Si',
                              className: 'btn-success'
                          },
                          cancel: {
                              label: 'No',
                              className: 'btn-danger'
                          }
                      },
                      callback: function (result) {
                          if(result == true){
                            /**/

                              let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_repuestos/";
                              EntradaUpdate.crear_repuestos(urldispositivo);
                          }
                      }
                    });

        });
        //kardex
        tablabody.on('click', '.btn-kardex', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
          bootbox.confirm({
                      message: "Esta seguro que desea crear estos dispositivos al kardex",
                      buttons: {
                          confirm: {
                              label: 'Si',
                              className: 'btn-success'
                          },
                          cancel: {
                              label: 'No',
                              className: 'btn-danger'
                          }
                      },
                      callback: function (result) {
                          if(result == true){
                            /**/

                              let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_kardex/";
                              let detalle_entrada= data_fila.id
                              //alert(urldispositivo);
                              EntradaUpdate.enviar_kardex(urldispositivo, detalle_entrada);
                          }
                      }
                    });

        });

        /** Uso de DRF**/
        let detalle_form = $('#detalleForm');
        detalle_form.submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: detalle_form.attr('action'),
                data: detalle_form.serialize(),
                success: function (response) {
                    tabla_temp.tabla.ajax.reload();
                },
            });
            document.getElementById("detalleForm").reset();
        });


    }

    static crear_dispositivos(urldispositivo) {
        $.ajax({
            type: 'POST',
            url: urldispositivo,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                bootbox.confirm("dispositivos creados exitosamente!",
                function(result){
                   location.reload();
                  });
            },
            error: function (response) {
              var mensaje = JSON.parse(response.responseText)
              alert( "Error al crear los dispositivo: " + mensaje['mensaje']);
            }
        });
    }

    static crear_repuestos(url_repuestos) {
        $.ajax({
            type: 'POST',
            url: url_repuestos,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                bootbox.confirm("repuestos creados exitosamente!",
                function(result){
                   location.reload();
                  });

            },
            error: function (response) {
              var mensaje = JSON.parse(response.responseText)
              alert( "Error al crear los Repuestos: " + mensaje['mensaje']);
            }

        });
    }
    static enviar_kardex(url_kardex, detalle_entrada){
      $.ajax({
          type: 'POST',
          url: url_kardex,
          data: {
              csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
              detalle_entrada: detalle_entrada
          },
          success: function (response) {
              bootbox.confirm("Dispositivos Ingresados al kardex",
              function(result){
                 location.reload();
                });

          },
          error: function (response) {
            var mensaje = JSON.parse(response.responseText)
            alert( "Error al crear los dispositivos al kardex: " + mensaje['mensaje']);
          }

      });

    }
    static validar_kardex(url_validar_kardex, tipo_dispositivo) {
        $.ajax({
            type: 'POST',
            url: url_validar_kardex,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                tipo_dispositivo: tipo_dispositivo
            },
            success: function (response) {
              $("[for='id_proveedor_kardex']").css({"visibility":"visible"});
              $('#id_proveedor_kardex').next(".select2-container").show();
              $("[for='id_estado_kardex']").css({"visibility":"visible"});
              $('#id_estado_kardex').next(".select2-container").show();
              $("[for='id_tipo_entrada_kardex']").css({"visibility":"visible"});
              $('#id_tipo_entrada_kardex').next(".select2-container").show();
            },
            error: function (response) {
              $("[for='id_proveedor_kardex']").css({"visibility":"hidden"});
              $('#id_proveedor_kardex').next(".select2-container").hide();
              $("[for='id_estado_kardex']").css({"visibility":"hidden"});
              $('#id_estado_kardex').next(".select2-container").hide();
              $("[for='id_tipo_entrada_kardex']").css({"visibility":"hidden"});
              $('#id_tipo_entrada_kardex').next(".select2-container").hide();
            }
        });
    }
}

class EntradaDetail {
    constructor() {
        let entrada_table = $('#entrada-table');
        var pk = entrada_table.data("pk");
        this.api_url = entrada_table.data("api");
        this.pk = entrada_table.data("pk");
        this.url_filtrada = this.api_url + "?entrada=" + this.pk;
        this.tabla = entrada_table.DataTable({
            searching: false,
            paging: true,
            ordering: false,
            processing: true,
            ajax: {
                url: this.url_filtrada,
                dataSrc: '',
                cache: true,
                data: function (params)
                {
                   return {
                     entrada: pk
                   };
                }
            },
            columns: [
                {data: "tdispositivo"},
                {data: "util"},
                {data: "repuesto"},
                {data: "desecho"},
                {data: "total"},
                {data: "precio_unitario"},
                {data: "precio_subtotal"},
                {data: "precio_descontado"},
                {data: "precio_total"},
                {data:"descripcion"},
                {data: "creado_por"},
                {data:" ",render: function(data, type, full, meta){
                    return "<a target='_blank' rel='noopener noreferrer' href="+full.dispositivo_list+" class='btn btn-success'>Listado Dispositivo</a>";
                }},
                {data:" " ,render: function(data, type, full, meta){
                    return "<a target='_blank' rel='noopener noreferrer' href="+full.repuesto_list+" class='btn btn-primary'>Listado Repuestos</a>";
                }}

            ]
        });

        let tablabody = $('#entrada-table tbody');
        let tabla_temp = this;

        tablabody.on('click', '.btn-editar', function () {
            let data_fila = this.tabla.row($(this).parents('tr')).data();
            location.href = data_fila.update_url;
        });

        tablabody.on('click', '.btn-dispositivo', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_dispositivos/";
            EntradaUpdate.crear_dispositivos(urldispositivo);
        });

        tablabody.on('click', '.btn-repuesto', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_repuestos/";
            EntradaUpdate.crear_repuestos(urldispositivo);
        });

        /** Uso de DRF**/
        let detalle_form = $('#detalleForm');
        detalle_form.submit(function (e) {
            e.preventDefault();

            $.ajax({
                type: "POST",
                url: detalle_form.attr('action'),
                data: detalle_form.serialize(),
                success: function (response) {
                    tabla_temp.tabla.ajax.reload();
                },
            });
            document.getElementById("detalleForm").reset();
        });
    }

    static crear_dispositivos(urldispositivo) {
        $.ajax({
            type: 'POST',
            url: urldispositivo,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log("dispositivos creados exitosamente");
            },
            error: function (response) {
                alert( "Error al crear los dispositivo:" + response.mensaje);
            }
        });
    }

    static crear_repuestos(url_repuestos) {
        $.ajax({
            type: 'POST',
            url: url_repuestos,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log("repuestos creados exitosamente");
            },
            error: function (response) {
                alert( "Error al crear los Repuestos:" + response.mensaje);
            }

        });
    }
}


(function (EntradaList, $, undefined) {
    var tabla = $('#entrada2-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel', 'pdf', 'copy'],
        processing: true,
        ajax: {
            url: $('#entrada2-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            cache: true,
            data: function () {
                return $('#entrada2-list-form').serializeObject(true);
            }
        },
        columns: [
            {data: "id"},
            {data: "tipo"},
            {data: "fecha", className: "nowrap"},
            {data: "en_creacion", className: "nowrap"},
            {data: "creada_por", className: "nowrap"},
            {data: "recibida_por", className: "nowrap"},
            {data: "proveedor", className: "nowrap"},
            {data: "urlSi", render: function(data, type, full, meta){
              if(full.en_creacion== "Si"){
                return "<a href="+data+" class='btn btn-block btn-success'>Abrir</a>";

              }else{
                return "<a href="+full.urlNo+" class='btn btn-block btn-success'>Abrir</a>";
              }

            }}
        ]


    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    EntradaList.init = function () {

        $('#spinner').hide();
        $('#entrada2-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

        $('#entrada2-table tbody').on('click', 'button', function () {
            var data = tabla.row($(this).parents('tr')).data();
            alert("Si funciona este boton");
        });

    }
}(window.EntradaList = window.EntradaList || {}, jQuery));

class EntradaDetalleDetail {
  constructor() {
      var validarDispositivos = $("#id_dispositivos_creados").val();
      var validarRepuestos = $("#id_repuestos_creados").val();
      if(validarDispositivos == "True"){
        document.getElementById("id_util").disabled = true;
      }
      if(validarRepuestos == "True"){
        document.getElementById("id_repuesto").disabled = true;
      }

  }
}

(function (SalidaDetalleList, $, undefined) {
    var valor = $('#salida-table').data("api");
    var pk = $('#salida-table').data("pk");
    var urlapi = valor + "?entrada=" + pk;
    var urlDispositivo =  $('#dispositivo-table').data("api");
    var urlAprobar =  $('#salida-table').data("apiaprobar");
    var urlRechazar =  $('#salida-table').data("apirechazar");
    var urlAprobarDispositivo = $('#dispositivo-table').data("apiaprobar");
    var urlRechazarDispositivo = $('#dispositivo-table').data("apirechazar");
    var urlTipoDispositivo = $('#dispositivo-table').data("tipo");
    var urlFinalizar = $('#salida-table').data("finalizar");
    var urlredireccion = $('#salida-table').data("redireccion");
    $('#id_entrada_detalle').empty();
    var tabla = $('#salida-table').DataTable({
        searching: true,
        paging: true,
        ordering: true,
        processing: true,
        ajax: {
            url: urlapi,
            dataSrc: '',
            cache: true,
            data: {
              desecho : pk
            }
        },
        columns: [
            {data: "tdispositivo"},
            {data: "cantidad"},
            {data: "entrada"},
            {data: "",render: function(data, type, full, meta){
              if(full.aprobado == false){
                return "<a id='desecho-aprobar' data-id="+full.id+"  class='btn btn-success btn-aprobar-desecho'>Aprobar</a>";
              }else{
                return "<span class='label label-success'>Aprobado</span>"
              }

            }},
            {data: "",render: function(data, type, full, meta){
              if(full.aprobado == false){
                 return "<a id='desecho-rechazar' data-id="+full.id+"  class='btn btn-warning btn-rechazar-desecho'>Rechazar</a>";
              }else{
                return "";
              }

            }},
        ]
    });

    /**/
    var tablaDispositivo = $('#dispositivo-table').DataTable({
        searching: true,
        paging: true,
        ordering: true,
        processing: true,
        ajax: {
            url: urlDispositivo,
            dataSrc: '',
            cache: true,
            data: {
              desecho : pk
            }
        },
        columns: [
            {data: "triage"},
            {data: "tipo"},
            {data: "",render: function(data, type, full, meta){
              if(full.aprobado == false){
                  return "<a id='desecho-aprobar' data-triage="+full.dispositivo+"  class='btn btn-success btn-aprobar-dispositivo'>Aprobar</a>";
              }else{
                return "<span class='label label-success'>Aprobado</span>"
              }


            }},
            {data: "",render: function(data, type, full, meta){
                if(full.aprobado == false){
                  return "<a id='desecho-rechazar' data-triage="+full.dispositivo+"  class='btn btn-warning btn-rechazar-dispositivo'>Rechazar</a>";
                }else{
                  return "";
                }

            }},
        ]
    });
    /**/
    /*Aprobar detalle de desecho*/
    tabla.on('click', '.btn-aprobar-desecho', function () {
            let data_fila = tabla.row($(this).parents('tr')).data();
            $.ajax({
              type: "POST",
              url: urlAprobar,
              dataType: 'json',
              data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                detalle:data_fila.id
              },
              success: function (response) {
                tabla.clear().draw();
                tabla.ajax.reload();
              },
              error: function (response) {
                var mensaje = JSON.parse(response.responseText)
                bootbox.alert(mensaje['mensaje']);
              }
          });


        });
        /**/
        /*Rechazar detalle de desecho*/
        tabla.on('click', '.btn-rechazar-desecho', function () {
                let data_fila = tabla.row($(this).parents('tr')).data();
                bootbox.confirm({
                    message: "¿Esta seguro que quiere rechazar este detalle de desecho?",
                    buttons: {
                        confirm: {
                            label: 'Yes',
                            className: 'btn-success'
                        },
                        cancel: {
                            label: 'No',
                            className: 'btn-danger'
                        }
                    },
                    callback: function (result) {
                        if (result == true) {
                          $.ajax({
                            type: "POST",
                            url: urlRechazar,
                            dataType: 'json',
                            data: {
                              csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                              detalle:data_fila.id
                            },
                            success: function (response) {
                              tabla.clear().draw();
                              tabla.ajax.reload();
                            },
                            error: function (response) {
                              var mensaje = JSON.parse(response.responseText)
                              bootbox.alert(mensaje['mensaje']);
                            }
                        });
                        }

                    }
                });


            });
            /**/
          /*Aprobar Dispositivo de desecho*/
          tablaDispositivo.on('click', '.btn-aprobar-dispositivo', function () {
                  let data_fila = tablaDispositivo.row($(this).parents('tr')).data();
                  $.ajax({
                    type: "POST",
                    url: urlAprobarDispositivo,
                    dataType: 'json',
                    data: {
                      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                      detalle:data_fila.id
                    },
                    success: function (response) {
                        tablaDispositivo.clear().draw();
                        tablaDispositivo.ajax.reload();
                    },
                    error: function (response) {
                      var mensaje = JSON.parse(response.responseText)
                      bootbox.alert(mensaje['mensaje']);
                    }
                });


              });
              /**/
              /*Rechazar Dispositivo de desecho*/
              tablaDispositivo.on('click', '.btn-rechazar-dispositivo', function () {
                      let data_fila = tablaDispositivo.row($(this).parents('tr')).data();
                      bootbox.confirm({
                          message: "¿Esta seguro que quiere rechazar este dispositivo?",
                          buttons: {
                              confirm: {
                                  label: 'Yes',
                                  className: 'btn-success'
                              },
                              cancel: {
                                  label: 'No',
                                  className: 'btn-danger'
                              }
                          },
                          callback: function (result) {
                            $.ajax({
                              type: "POST",
                              url: urlRechazarDispositivo,
                              dataType: 'json',
                              data: {
                                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                detalle:data_fila.id
                              },
                              success: function (response) {
                                tablaDispositivo.clear().draw();
                                tablaDispositivo.ajax.reload();
                              },
                              error: function (response) {
                                var mensaje = JSON.parse(response.responseText)
                                bootbox.alert(mensaje['mensaje']);
                              }
                          });


                          }
                      });



                  });
                  /**/
                  $('#id_tipo_dispositivo').change(function() {
                      if($('#id_tipo_dispositivo').val()==""){
                      }else{
                        /****/
                          var tipo = $(this).val();
                          var data_result = []
                          $("#id_entrada_detalle").select2("destroy");
                          $.ajax({
                            url:urlTipoDispositivo,
                            dataType:'json',
                            data:{
                              tipo_dispositivo:tipo,
                              desecho:0
                            },
                            error:function(){
                              console.log("Error");
                            },
                            success:function(data){
                                $('#id_entrada_detalle').empty();
                                data_result.push('<optgroup class="def-cursor" label="Entrada" data-tipo="Tipo" data-cantidad="Existencia">')
                                data_result.push('<option value="" data-tipo="-------" data-cantidad="-------">-------</option>');
                                for (var i in data){
                                  cantidad = data[i].existencia_desecho
                                  if(cantidad > 0){
                                    data_result.push('<option value='+data[i].id + ' data-tipo="'+data[i].tdispositivo+'" data-cantidad="'+cantidad+'">'+data[i].entrada+'</option>');
                                  }
                                }
                                data_result.push('</optgroup>')
                                $('#id_entrada_detalle').append(data_result);
                            },
                            type: 'GET'
                          }
                        );
                        $('#id_entrada_detalle').select2({
                          width: '100%',
                          tags: true,
                          createTag: function (params) {
                            return {
                                id: params.term,
                                text: params.term + $('#id_entrada_detalle').data(),
                                newOption: true
                            }
                          },
                          templateResult: function(data) {
                            var tipo = $(data.element).data('tipo');
                            var cantidad = $(data.element).data('cantidad');
                            var classAttr = $(data.element).attr('class');
                            var hasClass = typeof classAttr != 'undefined';
                            classAttr = hasClass ? ' ' + classAttr : '';

                              var $result = $(
                                  '<div class="row">' +
                                  '<div class="col-md-3 col-xs-6' + classAttr + '">' + data.text + '</div>' +
                                  '<div class="col-md-4 col-xs-6' + classAttr + '">' + tipo + '</div>' +
                                  '<div class="col-md-4 col-xs-6' + classAttr + '">' + cantidad + '</div>' +
                                  '</div>');
                              return $result;       
                          },
                          templateSelection: function (data) {
                            if(!data.id) { return data.text }
                            var tipo = $(data.element).data('tipo');
                            var cantidad = $(data.element).data('cantidad');

                            var result = data.text + ' - ' + tipo + '(' + cantidad + ')'
                            return result
                          }
                        }).on('select2:select', function (e) {
                          if (e.params.data.text != '') {

                            var id = $(this).attr('id');
                            var select2 = $("span[aria-labelledby=select2-" + id + "-container]");
                            select2.removeAttr('style');
                          }
                        }); 
                      }
                    });

    SalidaDetalleList.init = function () {
        $('#btn-terminar').click(function () {
            bootbox.confirm({
                message: "¿Esta seguro que quiere terminar la salida de desechos?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result == true) {
                      $.ajax({
                        type: "POST",
                        url: urlFinalizar,
                        dataType: 'json',
                        data: {
                          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                          id:pk
                        },
                        success: function (response) {
                             bootbox.alert(response.mensaje);
                             window.location= urlredireccion;
                        },
                        error: function (response) {
                          var mensaje = JSON.parse(response.responseText)
                          bootbox.alert(mensaje['mensaje']);
                        }
                    });

                    }

                }
            });


        });

        /** Uso de DRF**/
        $('#detalleForm').submit(function (e) {
            e.preventDefault()
            $.ajax({
                type: "POST",
                url: $('#detalleForm').attr('action'),
                data: $('#detalleForm').serialize(),
                success: function (response) {
                    console.log("datos ingresados correctamente");

                },
                error: function (response) {
                  var mensaje = JSON.parse(response.responseText)
                  bootbox.alert(mensaje.error[0]);
                }
            });
            $("#id_tipo_dispositivo").select2("destroy").select2();
            $("#id_tipo_dispositivo").select2("val", "");


            $("#id_entrada_detalle").select2("destroy").select2();
            $("#id_entrada_detalle").select2("val", "");
            $('#id_entrada_detalle').html('');
            tabla.clear().draw();
            tabla.ajax.reload();
            document.getElementById("detalleForm").reset();
        });
      /** uso de DRF**/
      $('#dispositivoForm').submit(function (e) {
          e.preventDefault()
         $.ajax({
              type: "POST",
              url: $('#dispositivoForm').attr('action'),
              data: $('#dispositivoForm').serialize(),
              success: function (response) {
                  console.log("datos ingresados correctamente");
              },
          });
          tablaDispositivo.clear().draw();
          tablaDispositivo.ajax.reload();
          document.getElementById("dispositivoForm").reset();
      });
    }
}(window.SalidaDetalleList = window.SalidaDetalleList || {}, jQuery));

class SolicitudMovimiento {
  constructor() {
    var url =  $('#recibido-kardex').data("url");
    $('#movimientos-table-body').DataTable({
      dom: 'lfrtipB',
      buttons: ['excel','pdf']
    });

    $('#btn-recibido').click(function (e) {
       e.preventDefault();
        bootbox.confirm({
            message: "¿Esta Seguro que quiere recibir esta Solicitud de Movimiento?",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-success'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result == true) {
                  $.ajax({
                      type: "POST",
                      url: $('#btn-recibido').attr('href'),
                      dataType: 'json',
                      data: {
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                        id: $('#btn-recibido').data("id")

                      },
                      success: function (response) {
                          location.reload();

                      },
                  });
                }

            }
        });
    });

    $('#aprobar-kardex').click(function (e) {
       e.preventDefault();
        bootbox.confirm({
            message: "¿Esta Seguro de aprobar esta peticion de dispositivos?",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-success'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result == true) {
                  $.ajax({
                      type: "POST",
                      url: $('#aprobar-kardex').attr('href'),
                      dataType: 'json',
                      data: {
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                        id: $('#aprobar-kardex').data("id"),
                        respuesta: 1

                      },
                      success: function (response) {
                        location.reload();
                      },
                  });
                }
            }
        });
    });

    $('#recibido-kardex').click(function (e) {
       e.preventDefault();
        bootbox.confirm({
            message: "¿Esta Seguro que desea rechazar estos dispositivos?",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-success'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result == true) {
                  $.ajax({
                      type: "POST",
                      url: $('#aprobar-kardex').attr('href'),
                      dataType: 'json',
                      data: {
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                        id: $('#aprobar-kardex').data("id"),
                        respuesta: 2

                      },
                      success: function (response) {
                          window.location.href = url;

                      },
                  });
                }
            }
        });
    });
  }
}


class SolicitudMovimientoUpdate {
    constructor() {
        var sel_dispositivos = $('#id_dispositivos');
        let api_url = sel_dispositivos.data('api-url');
        let etapa_inicial = sel_dispositivos.data('etapa-inicial');
        let estado_inicial = sel_dispositivos.data('estado-inicial');
        let tipo_dipositivo = sel_dispositivos.data('tipo-dispositivo');
        let slug = sel_dispositivos.data('slug');
        var cantidad = $("#solicitud-table").data("cantidad");
        $('#id_dispositivos').val("").trigger('change');
        var lista_triage = [];
        sel_dispositivos.select2({
            maximumSelectionLength : cantidad,
            placeholder: "Ingrese los triage",
            width : '50%'
        });
        let cantidad_dispositivos = sel_dispositivos;
        $('form').on('submit', function(e){
           let restante  = cantidad - cantidad_dispositivos.select2('data').length;

          if(cantidad_dispositivos.select2('data').length < cantidad){

            bootbox.alert("Aun faltan  "+ restante  +" dispositivos por ingresar");
            e.preventDefault();
          }
        });
        /*Scanner*/
        var inputStart, inputStop, firstKey, lastKey, timing, userFinishedEntering;
        var minChars = 3;

        // handle a key value being entered by either keyboard or scanner
        $("#area_scanner").keypress(function (e) {
            // restart the timer
            if (timing) {
                clearTimeout(timing);
            }

            // handle the key event
            if (e.which == 13) {
                // Enter key was entered

                // don't submit the form
                e.preventDefault();

                // has the user finished entering manually?
                if ($("#area_scanner").val().length >= minChars){
                    userFinishedEntering = true; // incase the user pressed the enter key
                    inputComplete();
                }
            }
            else {
                // some other key value was entered

                // could be the last character
                inputStop = performance.now();
                lastKey = e.which;
                // don't assume it's finished just yet
                userFinishedEntering = false;

                // is this the first character?
                if (!inputStart) {
                    firstKey = e.which;
                    inputStart = inputStop;

                    // watch for a loss of focus
                    $("body").on("blur", "#area_scanner", inputBlur);
                }

                // start the timer again
                timing = setTimeout(inputTimeoutHandler, 500);
            }
        });

        // Assume that a loss of focus means the value has finished being entered
        function inputBlur(){
            clearTimeout(timing);
            if ($("#area_scanner").val().length >= minChars){
                userFinishedEntering = true;
                inputComplete();
            }
        };


        // reset the page
        $("#reset").click(function (e) {
            e.preventDefault();
            resetValues();
        });

        function resetValues() {
            // clear the variables
            inputStart = null;
            inputStop = null;
            firstKey = null;
            lastKey = null;
            // clear the results
            inputComplete();
        }

        // Assume that it is from the scanner if it was entered really fast
        function isScannerInput() {
            return (((inputStop - inputStart) / $("#area_scanner").val().length) < 15);
        }

        // Determine if the user is just typing slowly
        function isUserFinishedEntering(){
            return !isScannerInput() && userFinishedEntering;
        }

        function inputTimeoutHandler(){
            // stop listening for a timer event
            clearTimeout(timing);
            // if the value is being entered manually and hasn't finished being entered
            if (!isUserFinishedEntering() || $("#area_scanner").val().length < 3) {
                // keep waiting for input
                return;
            }
            else{
                reportValues();
            }
        }

        // here we decide what to do now that we know a value has been completely entered
        function inputComplete(){
            // stop listening for the input to lose focus
            $("body").off("blur", "#area_scanner", inputBlur);
            // report the results
            reportValues();
        }

        function reportValues() {
            var inputMethod = isScannerInput() ? "Scanner" : "Keyboard";
             if(inputMethod == "Scanner"){
                var datos = {};
                var seleccion = new Array(cantidad);
                var triage = $("#area_scanner").val();
                 var mensaje = JSON.parse(triage);
                 datos['text'] = mensaje.triage;
                 datos['id'] = mensaje.id;
                 /*Api*/
                 $.ajax({
                   url:api_url,
                   dataType:'json',
                   data:{
                     etapa: etapa_inicial,
                     estado: estado_inicial,
                     triage: mensaje.triage
                   },
                   error:function(){
                     console.log("Error");
                   },
                   success:function(data){
                     if(data.length >0){
                       /*asignar datos*/
                       lista_triage.push(datos);
                       $("#area_scanner").val("");
                       inputStart = null;
                       inputStop = null;
                       firstKey = null;
                       lastKey = null;
                       sel_dispositivos.select2({
                           maximumSelectionLength : cantidad,
                           debug: true,
                           placeholder: "Ingrese los triage",
                           data:lista_triage,
                           processResults: function (data){
                             return {
                               results : data.map(lista_triage =>{
                                 return {id: lista_triage["value"], text:lista_triage["triage"]};
                               })
                             };
                           },
                           width : '100%'
                       });
                      for(var i = 0; i<(lista_triage.length);i++){
                          seleccion[i] = lista_triage[i].id;
                     }
                       $('#id_dispositivos').val(seleccion).trigger('change');
                       /**/

                     }else{
                       bootbox.alert("Este dispositivo no esta disponible");
                       $("#area_scanner").val("");

                     }
                   },
                   type: 'GET'
                 }
               );
                 /**/
             }
        }
        $("#area_scanner").focus();
        /*Fin scanner*/
        $("#btn-manual").click(function(e){
          $("#area_scanner").attr('type','hidden');
          $("[for='area_scanner']").css({"visibility":"hidden"});
          $('#id_dispositivos').val(" ").trigger('change');
          $("#btn-manual").css({"visibility":"hidden"});

          /**/
          sel_dispositivos.select2({
              maximumSelectionLength : cantidad,
              debug: true,
              placeholder: "Ingrese los triage",
              ajax: {
                  url: api_url,
                  dataType: 'json',
                  data: function (params) {
                      return {
                          search: params.term,
                          etapa: etapa_inicial,
                          estado: estado_inicial,
                          buscador: slug + "-" + params.term
                      };
                  },
                  processResults: function (data) {
                      return {
                          results: data.map(dispositivo => {
                              return {id: dispositivo["id"], text: dispositivo['triage']};
                          })
                      };
                  },
                  cache: true
              },
              width : '50%'
          });
          /**/

        });

    }
}

class SolicitudEstadoTipo {
  constructor() {
    /**Uso de tablas **/
    let paquete_tabla = $('#paquetes-table');
    let api_urlpaquete =$('#asignarDispositivo').data('urlpaquete');
    let salidapk = $('#asignarDispositivo').data('pk');
    let url_filtrada = api_urlpaquete + salidapk;
    var cambios_etapa =$('#asignarDispositivo').data('urlmovimiento');
    /****/
    this.asignarDispositivo = $('#asignarDispositivo');
    var tablaSignar = paquete_tabla.DataTable({
     processing:true,
     retrieve:true,
     ajax:{
       url:api_urlpaquete,
       dataSrc:'',
       cache:false,
       deferRender:true,
       processing: true,
       data: function () {
         return {
           salida: salidapk,
           tipo_dispositivo: $('#id_tipo').val(),
           aprobado:false
         }
       }
     },
     columns:[
       {data:"id",
          render: function(data, type, full, meta){
            return '<a href="'+full.urlPaquet+'">'+data+'</a>'

          }},
       {data:"tipo_paquete"},
       {data:"asignacion",render: function( data, type, full, meta ){
            for(var i = 0; i<(full.asignacion.length);i++){
                 var asignacionDispositivos = full.asignacion[i].dispositivo.triage;
           }

           if(asignacionDispositivos==undefined){
             asignacionDispositivos = "No cuenta con dispositivos";
           }
           return asignacionDispositivos;
         }},
       {data:"aprobado", render: function( data, type, full, meta){
        if(full.aprobado == true){
           return "Aprobado";
         }else{
           return "Pendiente"
         }
       }},
       {data:"id_paquete",
       render:function(data, type, full, name){
         return "<button id='buttonAsignar'"+"data-buttonSignar='"+full.id_paquete+"'class='btn btn-info btn-aprovar'>Aprovar</button>";
       }
      },
     ]
   });
   tablaSignar.on('click','.btn-aprovar', function () {
     let data_fila = tablaSignar.row($(this).parents('tr')).data();
     bootbox.confirm({
        message: "Esta Seguro de aprovar este paquete",
        buttons: {
            confirm: {
                label: 'Si',
                className: 'btn-success'
            },
            cancel: {
                label: 'No',
                className: 'btn-danger'
            }
        },
        callback: function (result) {
          if(result==true){
            $.ajax({
              type: "POST",
              url: cambios_etapa,
              data:{
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                paquete:data_fila.id_paquete
              },
              success: function (response){
                  bootbox.alert("Paquete y Dispositivos aprovados");
                  tablaSignar.clear().draw();
                  tablaSignar.ajax.reload();
              },
            });
          }

            console.log('This was logged in the callback: ' + result);
        }
      });

   });
    var api_url = this.asignarDispositivo.data('url');
    $('#id_tipo').change(function() {
      if($('#id_tipo').val()==""){
          $('#cuerpoPaquetes').css({"display":"none"});
      }else{
        /****/
        $('#cuerpoPaquetes').css({"display":"block"});
          var tipo = $(this).val();
          var urlDispositivo = api_url+"?buscador=&tipo="+tipo+"&estado=2&etapa=2&asignaciones=0";
          tablaSignar.clear().draw();
          tablaSignar.ajax.reload();
          $.ajax({
            url:urlDispositivo,
            dataType:'json',
            data:{
              format:'json'
            },
            error:function(){
              console.log("Error");
            },
            success:function(data){
                $('#id_dispositivo').empty();
                $('#id_dispositivo').append('<option value=""'+'>'+"---------"+'</option>');
                for (var i in data){
                  $('#id_dispositivo').append('<option value='+data[i].triage + '>'+data[i].triage+'</option>');
              }
             $('#id_dispositivo').val();
            },
            type: 'GET'
          }
        );
        /****/

      }

    });
    /***/
    let dispositivoPaqueteForm = $('#dispositivoPaqueteForm');
    let tipo = $('#id_tipo').val();
    dispositivoPaqueteForm.submit(function (e) {
      e.preventDefault();
      $.ajax({
        type: "POST",
        url: dispositivoPaqueteForm.attr('action'),
        data:dispositivoPaqueteForm.serialize(),
        success: function (response){
          bootbox.alert("Asignacion correctamente");
          tablaSignar.ajax.reload();
        },
      });
    });
    /***/
  }

}

class SalidasRevisarList {
  constructor() {
    /** Uso de tabla **/
    let revision_tabla = $('#salidasrevisar-table');
    let api_url_revision = $('#salidarevisionid').data('url');
    var tablaRevision = revision_tabla.DataTable({
      processing:true,
      retrieve:true,
      ajax:{
        url:api_url_revision +"?estado=1",
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
        data: function () {
          return {
            aprobada:false
          }
        }

      },
      columns:[
        {data:"salida", render: function( data, type, full, meta){
          return '<a href="'+full.urlSalida+'">'+data+'</a>'
        }},
        {data:"fecha_revision", render: function(data, type, full, meta){
         var newDate = new Date(full.fecha_revision);
         var options = {year: 'numeric', month:'long', day:'numeric', hour:'numeric',minute:'numeric'};
          return newDate.toLocaleDateString("es-Es",options);
        }},
        {data:"revisado_por"},
        {data:"estado"},
      ]

    });
  }
}

class Salidas {
  constructor() {
    let tabla_paquetes = $('#salidas-paquete-table');
    var disponible =0;
    var dispositivo_triage = 0;
    var urlrechazar_kardex = $("#id-reasignar").data("kardexrechazar");
    var urlraprobar_kardex = $("#id-reasignar").data("kardexaprobar");
    var url_salida= $("#salidas-table").data("url");
    var url_salida_paquete= $("#salidas-paquete-table").data("url");
    var salida_pk= $("#salidas-paquete-table").data("pk");
    var url_cuadrar = $("#salidas-paquete-table").data("cuadrar");
    var url_finalizar = $("#salidas-paquete-table").data("urlfin");
    var url_detail = $("#salidas-paquete-table").data("urldetail");
    var fecha = new Date();
    var dia = fecha.getDate();
    var mes = fecha.getMonth()+1;
    var year = fecha.getFullYear();
    if(dia<10){
        dia='0'+dia;
    }
    if(mes<10){
        mes='0'+mes;
    }
    var fecha = year+'-'+mes+'-'+dia;
    $('#id_fecha').val(fecha);
    $("[for='id_entrega']").css({"visibility":"hidden"});
    $("[for='id_garantia']").css({"visibility":"hidden"});
    $("[for='id_beneficiario']").css({"visibility":"hidden"});
    $('#id_garantia').next(".select2-container").hide();
    $('#id_beneficiario').next(".select2-container").hide();

    $('#id_entrega').click(function () {
        if ($("#id_entrega").is(':checked')) {
          $("[for='id_udi']").css({"visibility":"visible"});
          $("#id_udi").attr('type','visible');
          $("#id_udi").val(" ");
          $("#id_beneficiario").css({"visibility":"hidden"});
          $("[for='id_beneficiario']").css({"visibility":"hidden"});
          $('#id_beneficiario').next(".select2-container").hide();
        } else {
          $("#id_udi").attr('type','hidden');
          $("[for='id_udi']").css({"visibility":"hidden"});
          $("[for='id_beneficiario']").css({"visibility":"visible"});
          $("#id_beneficiario").css({"visibility":"visible"});
          $("#id_udi").val(" ");
          $('#id_beneficiario').next(".select2-container").show();
        }
    });
    $('#salidaform').on('submit', function(e){
      var udi = $("#id_udi").val();
      var beneficiario = $("#id_beneficiario").val();
      if ($("#id_entrega").is(':checked')) {
        if(udi.length == 0){
              bootbox.alert("Necesita Ingresar un UDI");
              e.preventDefault();
        }
      }else{
        if(tipoSalida == 7 || tipoSalidaText =='Garantia') {
            $("#id_beneficiario").val(" ");
        }else{
          if(beneficiario.length == 0){
            bootbox.alert("Necesita Ingresar un Beneficiario");
              e.preventDefault();
          }
        }
      }

    });

    $('#salidas-table').DataTable({
      dom: 'lfrtipB',
      buttons: ['excel','pdf'],
      ajax:{
        url:url_salida,
        dataSrc:'',
        cache:true,

      },
      columns:[
        {data:"id"},
        {data:"tipo_salida"},
        {data:"fecha"},
        {data:"estado"},
        {data:"escuela", render: function(data, type, full, meta){
          if(full.escuela===undefined){
            return " ";
          }else{
            return full.escuela;
          }

        }},
        {data:"beneficiario"},
        {data:"", render: function(data, type, full, meta){
          if(full.estado == 'Entregado'){
            return "<a target='_blank' rel='noopener noreferrer' href="+full.detail_url+" class='btn btn-success'>Abrir</a>";
          }else{
            return "<a target='_blank' rel='noopener noreferrer' href="+full.url+" class='btn btn-success'>Abrir</a>";
          }

        }}
      ]
    });

    var nueva_tabla = tabla_paquetes.DataTable({
      dom: 'lfrtipB',
      buttons: ['excel','pdf'],
      ajax:{
        url:url_salida_paquete,
        dataSrc:'',
        cache:true,
        data: function () {
          return {
            asignacion: salida_pk,
            desactivado:false
          }
        }

      },
      columns:[
        {data:"id"},
        {data:"tipo_paquete"},
        {data:"fecha_creacion", render: function(data, type, full, meta){
         var newDate = new Date(full.fecha_creacion);
         var options = {year: 'numeric', month:'long', day:'numeric', hour:'numeric',minute:'numeric'};
          return newDate.toLocaleDateString("es-Es",options);
        }},
        {data:"cantidad"},
        {data:"aprobado", render: function(data, type, full, meta){
          if(full.aprobado == true){
            return "<span class='label label-success'>Revisado</span>"

          }else{
            return "<span class='label label-danger'>No Revisado</span>"
          }
        }},
        {data:"", render: function(data, type, full, meta){
          if(full.tipo_salida == "Especial" ){
            return ""
          }else{
            if(full.usa_triage == "False"){
              if(full.aprobado == true){
                return " ";
              }else{
                return "<a id='conta-aprobar'  class='btn btn-success btn-aprobar-conta'>Aprobar</a>";
              }
            }else{
              return "<a target='_blank' rel='noopener noreferrer' href="+full.url_detail+" class='btn btn-success'>Ver Dispositivos</a>";
            }

          }
        }},
        {data:"", render: function(data, type, full, meta){
          if(full.aprobado ==false){
            if(full.usa_triage == "False"){
              return "<a id='conta-rechazar'  class='btn btn-warning btn-rechazar-conta'>Rechazar</a>";

            }else{
              return "<a target='_blank' rel='noopener noreferrer' href="+full.urlPaquet+" class='btn btn-primary'>Asignar Dispositivos</a>";
            }

          }else{
            return "";
          }

        }}
      ]
    });

    /**Boton Aprobar Dispositivos**/
    nueva_tabla.on('click','.btn-aprobar-conta', function () {
     let data_fila = nueva_tabla.row($(this).parents('tr')).data();
      $.ajax({
        type: "POST",
        url: urlraprobar_kardex,
        data:{
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          id_paquete:data_fila.id_paquete
        },
        success: function (response){
            bootbox.alert("Paquete aprovado");
            location.reload();
        },
      });

    } );
    /**Boton  de Rechazo de Dispositivos**/
    nueva_tabla.on('click','.btn-rechazar-conta', function () {
      let data_fila = nueva_tabla.row($(this).parents('tr')).data();
      /****/
     bootbox.confirm({
         message: "Esta seguro de rechazar el paquete?",
         buttons: {
             confirm: {
                 label: 'Si',
                 className: 'btn-success'
             },
             cancel: {
                 label: 'No',
                 className: 'btn-danger'
             }
         },
         callback: function (result) {
           if(result==true){
             console.log(urlrechazar);
             $.ajax({
               type: "POST",
               url: urlrechazar_kardex,
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 id_paquete:data_fila.id_paquete
               },
               success: function (response){
                  bootbox.alert("Paquete Rechazado");
                  location.reload();
               },
             });
           }

             console.log('This was logged in the callback: ' + result);
         }
       });
      /****/
    });
//select2
    this.asig_salidas =$('#id_entrada');
    let api_urlentrada=this.asig_salidas.data('api-url');
    let beneficiario = $('#salidas-paquete-table').data("beneficiario");
    let tipo =$('#salidas-paquete-table').data("tipo");
    this.asig_salidas.select2(
      {
        placeholder:"Ingrese la Entrada",
        debug:true,
        width:'100%',
        ajax:{
          url:api_urlentrada,
          dataType:'json',
          data: function (params){
            return{
              search:params.term,
              proveedor:beneficiario,
              tipo:3,
              buscador:params.term

            };
          },
          processResults: function (data){
            return {
              results: data.map(salida => {
                  return {
                    id:salida["id"],
                    text:salida["id"]
                  }
              })
            };
          },
          initSelection: function (data){
            var nuevo = [];
            nuevo.push({id:0, text:0})
          },
          cache:true
        }
      }
    );
    if(tipo != 3){
      $("#id_entrada").next(".select2-container").hide();
      $("[for='id_entrada']").css({"visibility":"hidden"});
    }

    /**En Creacion**/

    $('#id_en_creacion').click(function () {
        if ($("#id_en_creacion").is(':checked')) {

        } else {
          bootbox.confirm({
                      message: "Esta Seguro que quiere Terminar la Creacion de Salida",
                      buttons: {
                          confirm: {
                              label: 'Si',
                              className: 'btn-success'
                          },
                          cancel: {
                              label: 'No',
                              className: 'btn-danger'
                          }
                      },
                      callback: function (result) {
                          if(result == true){
                            /**/
                           $.ajax({
                                type: 'POST',
                                url: url_cuadrar,
                                dataType: 'json',
                                data: {
                                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                    primary_key :salida_pk,
                                    tipo:tipo
                                },
                                success: function (response) {
                                     $.ajax({
                                       type: "POST",
                                       url: url_finalizar,
                                       dataType: 'json',
                                       data: {
                                           csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                           salida :salida_pk,
                                       },
                                       success: function (response){
                                        window.location.href = url_detail;
                                       },
                                     });
                                     /***/
                                },
                                error: function (response) {
                                     var jsonResponse = JSON.parse(response.responseText);
                                     bootbox.alert(jsonResponse["mensaje"]);
                                     document.getElementById("id_en_creacion").checked = true;
                                }
                            });
                            /**/

                          }else{
                              document.getElementById("id_en_creacion").checked = true;
                          }
                      }
                    });
        }
    });

    /***/

      var url_kardex = $('#id-reasignar').data('kardex');
      $("#label_kardex").css({"visibility":"hidden"});
      $('#id_tipo_paquete').change(function(){
        var cantidad  = $('#id_cantidad').val();
        var tipo_paquete = $(this).val();
        $.ajax({
          type: "POST",
          url: url_kardex,
          data:{
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            tipo_dispositivo:tipo_paquete
          },
          success: function (response){
            if(response['mensaje']=="Usa Triage"){
              $('#id_cantidad').val("");
                dispositivo_triage =1;
                $("#label_kardex").css({"visibility":"hidden"});
                $('#existencia_kardex').html(" ");
            }else{
              $('#id_cantidad').val("");
              $("#label_kardex").css({"visibility":"visible"});
               $('#existencia_kardex').html("<b>"+response['mensaje']);
               disponible = parseInt(response['mensaje']);
            }
          },
          error:function(error){
          },
        });
      });
    /***/
    $('#id_cantidad').focusout(function() {
      if (dispositivo_triage == 1){
        $('#paquetes_add').css({"visibility":"visible"});
        $("#label_kardex").css({"visibility":"hidden"});
         $('#existencia_kardex').html(" ");
         dispositivo_triage=0;
      }else{
        var cantidad  = $('#id_cantidad').val();
        if(cantidad > disponible){
          $('#paquetes_add').css({"visibility":"hidden"});
          $('#id_cantidad').val("");
          bootbox.alert("No has dipositivos suficientes para asignar");
        }else{
           $('#paquetes_add').css({"visibility":"visible"});
        }
      }

    });
    /**/
    $('#id_tipo_salida').change(function(){
      var tipoSalida = $(this).val();
      var tipoSalidaText = $('#id_tipo_salida option:selected').text()
      if(tipoSalida == 3 || tipoSalidaText =='Especial'){
        $("[for='id_entrega']").css({"visibility":"visible"});
        $("#id_entrega").css({"visibility":"visible"});
        /**/
        $("[for='id_udi']").css({"visibility":"visible"});
        $("#id_udi").attr('type','visible');
        $("#id_udi").val(" ");
        $("#id_beneficiario").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"hidden"});
        $('#id_beneficiario').next(".select2-container").hide();
        $("[for='id_garantia']").css({"visibility":"hidden"});
        $('#id_garantia').next(".select2-container").hide();
      }else if(tipoSalida == 4 || tipoSalidaText =='A terceros') {
        $("[for='id_entrega']").css({"visibility":"hidden"});
        $("#id_entrega").css({"visibility":"hidden"});
        $("#id_entrega").prop('checked',true);
        /**/
        $("#id_udi").attr('type','hidden');
        $("[for='id_udi']").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"visible"});
        $("#id_beneficiario").css({"visibility":"visible"});
        $("#id_udi").val(" ");
        $('#id_beneficiario').next(".select2-container").show();
        $("[for='id_garantia']").css({"visibility":"hidden"});
        $('#id_garantia').next(".select2-container").hide();
      }else if(tipoSalida == 7 || tipoSalidaText =='Garantia') {
        $("[for='id_entrega']").css({"visibility":"hidden"});
        $("#id_entrega").css({"visibility":"hidden"});
        $("#id_entrega").prop('checked',false);
        $("[for='id_garantia']").css({"visibility":"visible"});
        $('#id_garantia').next(".select2-container").show();
        /**/
        $("#id_udi").attr('type','hidden');
        $("[for='id_udi']").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"hidden"});
        $("#id_beneficiario").css({"visibility":"hidden"});
        $("#id_udi").val(" ");
        $('#id_beneficiario').next(".select2-container").hide();
      } else {
        $("[for='id_entrega']").css({"visibility":"hidden"});
        $("#id_entrega").css({"visibility":"hidden"});
        $("#id_entrega").prop('checked',true);
        /**/
        $("[for='id_udi']").css({"visibility":"visible"});
        $("#id_udi").attr('type','visible');
        $("#id_udi").val(" ");
        $("#id_beneficiario").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"hidden"});
        $("#id_beneficiario").attr('type','visible');
        $('#id_beneficiario').next(".select2-container").hide();
        /**/
        $("[for='id_garantia']").css({"visibility":"hidden"});
        $('#id_garantia').next(".select2-container").hide();
      }
    });
    /**Reasignar**/
    var asignacion =   $('#id-reasignar').data('entrega');
    var urlrechazar = $('#id-reasignar').data('urlreasignar');
    var urldonantes = $('#id-reasignar').data('urldonantes');
    if(asignacion == "None"){
      var mensaje = "Ingrese el UDI a Reasignar";
        var es_beneficiario = false;
    }else{
      var mensaje = "Ingrese el Beneficiario a Reasignar";
      var es_beneficiario = true;
    }
    if(es_beneficiario == true){
      $('#id-reasignar').click( function(){
        $.ajax({
             url:urldonantes,
             data:function (){
             return {
               asignacion: salida_pk,
             }
            },
             error:function(error){
               console.log(error);
             },
             success:function(data){
               var listaDeDonantes = [];
               for (var i in data){
                 var donante = {}
                 donante['text'] = data[i].nombre;
                 donante['value'] =data[i].id;
                 listaDeDonantes.push(donante);
             }
               bootbox.prompt({
             title: "Seleccione el Donante",
             inputType: 'select',
             inputOptions: listaDeDonantes,
             callback: function (result) {
                 //
                 $.ajax({
                  type: "POST",
                  url:urlrechazar,
                  data:{
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                    data:result,
                    id_salida:salida_pk,
                    beneficiario:es_beneficiario
                  },
                  success:function (response){
                    bootbox.alert(response.mensaje);
                    location.reload();

                  },
                  error: function (response) {
                       bootbox.alert("Seleccione un  Donante dela lista");

                  }
                });
                 //
             }
             });

             },
             type: 'GET'
           }
         );
       });
    }else{
      $('#id-reasignar').click( function(){
       bootbox.prompt({
           title: mensaje,
           callback: function (result) {
             if (result) {
               $.ajax({
                type: "POST",
                url:urlrechazar,
                data:{
                  csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                  data:result,
                  id_salida:salida_pk,
                  beneficiario:es_beneficiario
                },
                success:function (response){
                  bootbox.alert(response.mensaje);
                  location.reload();

                },
                error: function (response) {
                     var jsonResponse = JSON.parse(response.responseText);
                     bootbox.alert(jsonResponse["mensaje"]);
                }
              });
             }
           }
         });

       });
    }

  }
}
class PaquetesRevisionList {
  constructor() {
    let  paquetes_revision_tabla = $('#salida-paquetes-revision');
    let api_paquetes_revision = $('#paquetes-revision').data('url');
    let urlraprobar = $('#paquetes-revision').data('urlaprobar');
    let urlrechazar = $('#paquetes-revision').data('urlrechazar');
    var api_paquete_salida= $('#paquetes-revision').data('id');
    let api_aprobar_salida=$('#aprobar-btn').data('url')
    let  dispositivo_revision_tabla = $('#dispositivo-salida-paquetes-revision');
    //tablas kardexa
    let api_paquetes_revision_kardex = $('#paquetes-revision-kardex').data('url');
    let paquete_revision_aprobado_kardex = $('#dispositivo-salida-paquetes-revision-kardex');
    let paquetes_revision_tabla_kardex = $('#salida-paquetes-revision-kardex');
    var  tablaPaquetes = paquetes_revision_tabla.DataTable({
      processing:true,
      retrieve:true,
      ajax:{
        url:api_paquetes_revision,
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
        data: function () {
          return {
            salida:api_paquete_salida,
            aprobado:true
          }
        }
      },
      columns:[
        {data:"dispositivo"},
        {data:"tipo", render: function(data,type, full, meta){
          return data
        }} ,
        {data:" " ,render: function(data, type, full, meta){
            return "<a id='conta-aprobar' data-triage="+full.dispositivo+"  class='btn btn-success btn-aprobar-conta'>Aprobar</a>";
        }},
        {data:" " ,render: function(data, type, full, meta){
            return "<a id='conta-rechazar' data-paquete="+full.paquete+" data-triage="+full.dispositivo+"  class='btn btn-warning btn-rechazar-conta'>Rechazar</a>";
        }}
          ]

    });
    /****/
    var  tablaPaquetesDispositivos = dispositivo_revision_tabla.DataTable({
      processing:true,
      retrieve:true,
      ajax:{
        url:api_paquetes_revision,
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
        data: function () {
          return {
            listo:api_paquete_salida,
          }
        }
      },
      columns:[
        {data:"dispositivo"},
        {data:"tipo", render: function(data,type, full, meta){
          return data
        }} ,
          ]
    });

    /**Boton Aprobar Dispositivos**/
    tablaPaquetes.on('click','.btn-aprobar-conta', function () {
      let data_fila = tablaPaquetes.row($(this).parents('tr')).data();
      $.ajax({
        type: "POST",
        url: urlraprobar,
        data:{
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          triage:data_fila.dispositivo
        },
        success: function (response){
            bootbox.alert("Dispositivos aprovados");
            location.reload();
        },
      });

    });
    /**Boton  de Rechazo de Dispositivos**/
    tablaPaquetes.on('click','.btn-rechazar-conta', function () {
      let data_fila = tablaPaquetes.row($(this).parents('tr')).data();
      /****/
      bootbox.confirm({
         message: "Esta seguro de rechazar el dispositivo",
         buttons: {
             confirm: {
                 label: 'Si',
                 className: 'btn-success'
             },
             cancel: {
                 label: 'No',
                 className: 'btn-danger'
             }
         },
         callback: function (result) {
           if(result==true){
             $.ajax({
               type: "POST",
               url: urlrechazar,
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 triage:data_fila.dispositivo
               },
               success: function (response){
                 var id_comentario = $("#paquetes-revision").data('id');
                 var url = $("#paquetes-revision").data('urlhistorico');
                 bootbox.prompt({
                   title: "Por que rechazo este dispositivo?",
                   inputType: 'textarea',
                   callback: function (result) {
                     if (result) {
                       crear_historial_salidas(url, id_comentario, result);
                     }
                   }
                 });
               },
             });
           }

             console.log('This was logged in the callback: ' + result);
         }
       });
      /****/
    });
    /** Boton de Historial **/
    var crear_historial_salidas = function(url, id_comentario, comentario){
      var data = {
        "id_comentario":id_comentario,
        "comentario":"El Dispositivo con Triage: "+ $("#conta-rechazar").data('triage')+" del paquete no: "+$("#conta-rechazar").data('paquete') +" "+ comentario
      }

      $.post(url, JSON.stringify(data)).then(function (response){
      var fecha = new Date(response.fecha);
      var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear()+","+response.usuario);
      var td = $('<td></td>').text(response.comentario);
      var tr = $('<tr></tr>').append(td).append(td_data);
      $('#body-salidas-' + id_comentario).append(tr);
      location.reload();
    },function(response){
      alert("Error al crear datos");
    });
    }
    $(".SalidaHistorico-btn").click( function(){
      var id_comentario = $(this).data('id');
      var url = $(this).data('url');
      bootbox.prompt({
        title: "Historial de Ofertas",
        inputType: 'textarea',
        callback: function (result) {
          if (result) {
            crear_historial_salidas(url, id_comentario, result);
          }
        }
      });
    });
    /**Botones de  Aprobacion**/
    $("#rechazar-btn").click( function(){
      bootbox.confirm({
       message: "Esta salida sera rechazada",
       buttons: {
           confirm: {
               label: 'Si',
               className: 'btn-success'
           },
           cancel: {
               label: 'No',
               className: 'btn-danger'
           }
       },
       callback: function (result) {

           console.log('This was logged in the callback: ' + result);
       }
     });

    });
    $("#aprobar-btn").click( function(){
      bootbox.confirm({
       message: "Esta  seguro que desea aprobar esta salida?",
       buttons: {
           confirm: {
               label: 'Si',
               className: 'btn-success'
           },
           cancel: {
               label: 'No',
               className: 'btn-danger'
           }
       },
       callback: function (result) {
         if(result==true){
           $.ajax({
             type: "POST",
             url: api_aprobar_salida+api_paquete_salida+"/aprobar_revision/",
             data:{
               csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
               salida:api_paquete_salida
             },
             success: function (response){
                 bootbox.alert(response.mensaje);
             },
             error: function (response) {
                  var jsonResponse = JSON.parse(response.responseText);
                  bootbox.alert(jsonResponse["mensaje"]);

             }
           });
         }

           console.log('This was logged in the callback: ' + result);
       }
     });
    });
    /*Tablas de Kardex*/
    //Tabla paquetes diponibles de kardex
    var  tablaPaquetesKardex = paquetes_revision_tabla_kardex.DataTable({
      processing:true,
      retrieve:true,
      ajax:{
        url:api_paquetes_revision_kardex,
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
        data: function () {
          return {
            salida:api_paquete_salida,
            aprobado_kardex:true,
            aprobado:false
          }
        }
      },
      columns:[
        {data:"id"},
        {data:"tipo_paquete", render: function(data,type, full, meta){
          return data
        }} ,
        {data:" " ,render: function(data, type, full, meta){
            return "<a id='conta-aprobar' data-triage="+full.dispositivo+"  class='btn btn-success btn-aprobar-conta-kardex'>Aprobar</a>";
        }},
        {data:" " ,render: function(data, type, full, meta){
            return "<a id='conta-rechazar' data-paquete="+full.paquete+" data-triage="+full.dispositivo+"  class='btn btn-warning btn-rechazar-conta-kardex'>Rechazar</a>";
        }}
          ]

    });
    //Tabla de Paquetes aprobados
    var  tablaPaquetesDispositivosKardex = paquete_revision_aprobado_kardex.DataTable({
      processing:true,
      retrieve:true,
      ajax:{
        url:api_paquetes_revision_kardex,
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
        data: function () {
          return {
            salida:api_paquete_salida,
            aprobado:true,
            aprobado_kardex:true
          }
        }
      },
      columns:[
        {data:"id"},
        {data:"tipo_paquete", render: function(data,type, full, meta){
          return data
        }} ,
          ]
    });

    /**Boton Aprobar, paquetes de tipo kardex**/
    tablaPaquetesKardex.on('click','.btn-aprobar-conta-kardex', function () {
      let data_fila = tablaPaquetesKardex.row($(this).parents('tr')).data();
      $.ajax({
        type: "POST",
        url: urlraprobar,
        data:{
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          paquete:data_fila.id_paquete,
          kardex:true
        },
        success: function (response){
            bootbox.alert("Paquete aprovado");
            location.reload();
        },
      });

    });
    /**Boton  de Rechazo, Paquetes, tipo kardex**/
    tablaPaquetesKardex.on('click','.btn-rechazar-conta-kardex', function () {
      let data_fila = tablaPaquetesKardex.row($(this).parents('tr')).data();
      /****/
     bootbox.confirm({
         message: "Esta seguro de rechazar este paquete",
         buttons: {
             confirm: {
                 label: 'Si',
                 className: 'btn-success'
             },
             cancel: {
                 label: 'No',
                 className: 'btn-danger'
             }
         },
         callback: function (result) {
           if(result==true){
             $.ajax({
               type: "POST",
               url: urlrechazar,
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 paquete:data_fila.id_paquete,
                 kardex:true
               },
               success: function (response){
                var id_comentario = $("#paquetes-revision").data('id');
                 var url = $("#paquetes-revision").data('urlhistorico');
                 bootbox.prompt({
                   title: "Por que rechazo este dispositivo?",
                   inputType: 'textarea',
                   callback: function (result) {
                     if (result) {
                       crear_historial_salidas(url, id_comentario, result);
                     }
                   }
                 });
               },
             });
           }

             console.log('This was logged in the callback: ' + result);
         }
       });
      /****/
    });

  }
}
class PaqueteDetail {
  constructor() {
    let tablabodyRechazar = $("#rechazar-dispositivo tbody tr");
    var urlCambio = $("#salida-id").data('url');
    var urlAprobar = $("#salida-id").data('urlaprobar');
    var lista_triage = [];
    var estado_inicial = $('#id_dispositivos').data('estado-inicial');
    tablabodyRechazar.on('click','.btn-rechazar', function () {
      let data_triage = $(this).attr("data-triage");
      let data_paquete=$(this).attr("data-paquete");
      bootbox.confirm({
         message: "Esta seguro de rechazar el dispositivo",
         buttons: {
             confirm: {
                 label: 'Si',
                 className: 'btn-success'
             },
             cancel: {
                 label: 'No',
                 className: 'btn-danger'
             }
         },
         callback: function (result) {
           if(result==true){
             $.ajax({
               type: "POST",
               url: urlCambio,
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 triage:data_triage,
                 paquete:data_paquete
               },
               success: function (response){
                 var id_comentario = $("#salida-id").data('id');
                 var url = $("#salida-id").data('urlhistorico');

                 bootbox.prompt({
                   title: "Por que rechazo este dispositivo?",
                   inputType: 'textarea',
                   callback: function (result) {
                     if (result) {
                       crear_historial_salidas(url, id_comentario, result);
                     }
                   }
                 });
               },
             });
           }

             console.log('This was logged in the callback: ' + result);

         }
       });
    });
    /****/
    tablabodyRechazar.on('click','.btn-aprobar', function () {
      let data_triage = $(this).attr("data-triage");
      let data_paquete=$(this).attr("data-paquete");
      let data_idpaquete=$(this).attr("data-idpaquete");
      bootbox.confirm({
         message: "Esta seguro de aprobar el dispositivo",
         buttons: {
             confirm: {
                 label: 'Si',
                 className: 'btn-success'
             },
             cancel: {
                 label: 'No',
                 className: 'btn-danger'
             }
         },
         callback: function (result) {
           if(result==true){
             $.ajax({
               type: "POST",
               url: urlAprobar,
               dataType: 'json',
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 triage:data_triage,
                 paquete:data_paquete,
                 idpaquete:data_idpaquete
               },
               success: function (response){
                 bootbox.alert(response.mensaje);
                  location.reload();
               },
               error: function (response){
                 var jsonResponse = JSON.parse(response.responseText);
                 bootbox.alert(jsonResponse["mensaje"]);
               }
             });
           }

             console.log('This was logged in the callback: ' + result);
         }
       });
    });
    /****/
    var crear_historial_salidas = function(url, id_comentario, comentario){
      var data = {
        "id_comentario":id_comentario,
        "comentario":"El Dispositivo con Triage: "+ $("#id-rechazar").data('triage')+" del paquete no: "+$("#id-rechazar").data('triagepaquete') +" "+ comentario
      }

      $.post(url, JSON.stringify(data)).then(function (response){
      var fecha = new Date(response.fecha);
      var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear()+","+response.usuario);
      var td = $('<td></td>').text(response.comentario);
      var tr = $('<tr></tr>').append(td).append(td_data);
    $('#body-salidas-' + id_comentario).append(tr);
    location.reload();

    },function(response){
      alert("Error al crear datos");
    });
    }
    /****/
    this.asig_dispositivos = $('#id_dispositivos');
    let api_url = this.asig_dispositivos.data('api-url');
    let etapa_inicial = 2;
    let tipo_dipositivo = this.asig_dispositivos.data('tipo-dispositivo');
    let slug = this.asig_dispositivos.data('slug');
    let cantidad = this.asig_dispositivos.data('cantidad');
    let cantidad_disponible = $('#rechazar-dispositivo').data('dispo');
    let cantidad_asignar = cantidad - cantidad_disponible;
    if(cantidad_asignar == 0){
      var activar = true
    }else{
      var activar = false
    }
    this.asig_dispositivos.select2({
        disabled :activar,
        maximumSelectionLength : cantidad_asignar,
        debug:true,
        placeholder:"Ingrese Triage",
        width: '100%',
        ajax:{
          url:api_url,
          dataType:'json',
          data: function (params){
            return{
              search:params.term,
              etapa:etapa_inicial,
              tipo:tipo_dipositivo,
              estado:1,
              buscador:slug +"-"+params.term
            };
          },
          processResults: function (data) {
            return {
              results: data.map(dispositivo => {
                return {id:dispositivo["id"], text:dispositivo['triage']};
              })
            };
          },
          cache: true
        }

    });
    let cantidad_dispositivos = this.asig_dispositivos;
    $('form').on('submit', function(e){
      let restante = cantidad_asignar - cantidad_dispositivos.select2('data').length;
      if(cantidad_dispositivos.select2('data').length < cantidad_asignar){
        bootbox.alert("Aun faltan  "+ restante  +" dispositivos por ingresar");
        e.preventDefault();
      }
    });
    /****/
    //Scanner
    var inputStart, inputStop, firstKey, lastKey, timing, userFinishedEntering;
      var minChars = 3;

      // handle a key value being entered by either keyboard or scanner
      $("#area_scanner").keypress(function (e) {
          // restart the timer
          if (timing) {
              clearTimeout(timing);
          }

          // handle the key event
          if (e.which == 13) {
              // Enter key was entered

              // don't submit the form
              e.preventDefault();

              // has the user finished entering manually?
              if ($("#area_scanner").val().length >= minChars){
                  userFinishedEntering = true; // incase the user pressed the enter key
                  inputComplete();
              }
          }
          else {
              // some other key value was entered

              // could be the last character
              inputStop = performance.now();
              lastKey = e.which;
              // don't assume it's finished just yet
              userFinishedEntering = false;

              // is this the first character?
              if (!inputStart) {
                  firstKey = e.which;
                  inputStart = inputStop;

                  // watch for a loss of focus
                  $("body").on("blur", "#area_scanner", inputBlur);
              }

              // start the timer again
              timing = setTimeout(inputTimeoutHandler, 500);
          }
      });

      // Assume that a loss of focus means the value has finished being entered
      function inputBlur(){
          clearTimeout(timing);
          if ($("#area_scanner").val().length >= minChars){
              userFinishedEntering = true;
              inputComplete();
          }
      };


      // reset the page
      $("#reset").click(function (e) {
          e.preventDefault();
          resetValues();
      });

      function resetValues() {
          // clear the variables
          inputStart = null;
          inputStop = null;
          firstKey = null;
          lastKey = null;
          // clear the results
          inputComplete();
      }

      // Assume that it is from the scanner if it was entered really fast
      function isScannerInput() {
          return (((inputStop - inputStart) / $("#area_scanner").val().length) < 15);
      }

      // Determine if the user is just typing slowly
      function isUserFinishedEntering(){
          return !isScannerInput() && userFinishedEntering;
      }

      function inputTimeoutHandler(){
          // stop listening for a timer event
          clearTimeout(timing);
          // if the value is being entered manually and hasn't finished being entered
          if (!isUserFinishedEntering() || $("#area_scanner").val().length < 3) {
              // keep waiting for input
              return;
          }
          else{
              reportValues();
          }
      }

      // here we decide what to do now that we know a value has been completely entered
      function inputComplete(){
          // stop listening for the input to lose focus
          $("body").off("blur", "#area_scanner", inputBlur);
          // report the results
          reportValues();
      }

      function reportValues() {
          var inputMethod = isScannerInput() ? "Scanner" : "Keyboard";
           if(inputMethod == "Scanner"){
              var datos = {};
              var seleccion = new Array(cantidad);
              var triage = $("#area_scanner").val();
               var mensaje = JSON.parse(triage);
               datos['text'] = mensaje.triage;
               datos['id'] = mensaje.id;
               /*Api*/
               $.ajax({
                 url:api_url,
                 dataType:'json',
                 data:{
                   etapa: etapa_inicial,
                   estado: estado_inicial,
                   id: mensaje.id
                 },
                 error:function(){
                   console.log("Error");
                 },
                 success:function(data){
                   if(data.length >0){
                     /*asignar datos*/
                     lista_triage.push(datos);
                     $("#area_scanner").val("");
                     inputStart = null;
                     inputStop = null;
                     firstKey = null;
                     lastKey = null;
                     $('#id_dispositivos').select2({
                         maximumSelectionLength : cantidad,
                         debug: true,
                         placeholder: "Ingrese los triage",
                         data:lista_triage,
                         processResults: function (data){
                           return {
                             results : data.map(lista_triage =>{
                               return {id: lista_triage["value"], text:lista_triage["triage"]};
                             })
                           };
                         },
                         width : '100%'
                     });
                    for(var i = 0; i<(lista_triage.length);i++){
                        seleccion[i] = lista_triage[i].id;
                   }
                     $('#id_dispositivos').val(seleccion).trigger('change');
                     /**/

                   }else{
                     bootbox.alert("Este dispositivo no esta disponible");
                     $("#area_scanner").val("");

                   }
                 },
                 type: 'GET'
               }
             );
               /**/
           }
      }
      $("#area_scanner").focus();

    //Fin Scanner

  }
}
class RepuestosList {
  constructor() {
    $('#repuesto-list').submit(function (e) {
      e.preventDefault();
      var url_repuestos = $("#repuesto-list").attr('action');
      let repuesto_tabla = $("#repuesto-table");

      var no=$('#id_id').val();
      var tipo = $('#id_tipo option:selected').val();
      var marca = $('#id_marca option:selected').val();
      var modelo = $('#id_modelo').val();
      var tarima = $('#id_tarima option:selected').val();

      if($('#qr-botton').length){
        let url = $("#qr-botton").data("url")+"?id="+no+"&tarima="+tarima+"&tipo="+tipo+"&marca="+marca+"&modelo="+modelo;
        document.getElementById("qr-botton").setAttribute("href", url);
        $('#qr-botton').css({"display":"block"});
      }

      var tabla = repuesto_tabla.DataTable({
        destroy:true,
        searching:true,
        paging:true,
        ordering:true,
        processing:true,
        ajax:{
          url:url_repuestos,
          dataSrc:'',
          cache:true,
          data: function() {
            return $('#repuesto-list').serializeObject(true);
          }
        },
        columns:[
          {data: "No", render: function(data, type, full, meta){
            return '<a href="'+full.url+'">'+data+'</a>'
          }},
          {data:"tipo"},
          {data:"descripcion"},
          {data:"marca"},
          {data:"modelo"},
          {data:"tarima"},
          {data:"estado"},
          {data:"", className:"nowrap", render:function(data, type, full, meta){
            if(full.valido == true){
              return ""
            }else{
              return "<button  id='button-repuesto' class='btn btn-info repuesto-btn'>Asignar</button>"
            }
          }}
        ]
      });

      tabla.clear().draw();
      tabla.ajax.reload();

      tabla.on('click','.repuesto-btn',function () {
        let repuesto = tabla.row($(this).parents('tr')).data();
        bootbox.prompt("Ingrese el Triage del Dispositivo", function(result){
            $.ajax({
             type: "POST",
             url:url_repuestos +"asignar_repuesto/",
             data:{
               csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
               repuesto:repuesto.id,
               triage:result
             },
             success:function (response){
               tabla.ajax.reload();
             }
           });
         });
      });

    });
  }
}
class DispositivoList {
  constructor() {
    $('#dispositivo-list-form').submit(function (e) {
        e.preventDefault();
        /**/
        var tablaDispositivos = $('#dispositivo-table').DataTable({
           dom: 'lfrtipB',
           destroy:true,
           buttons: ['excel', 'pdf'],
           processing: true,
           ajax: {
               url: $('#dispositivo-list-form').attr('action'),
               deferRender: true,
               dataSrc: '',
               cache: true,
               data: function () {
                   return $('#dispositivo-list-form').serializeObject(true);
               }
           },
           columns: [

               {data: "triage", render: function(data, type, full, meta){
                 return '<a href="'+full.url+'">'+data+'</a>'

               }},
               {data: "tipo", className: "nowrap"},
               {data: "marca", className: "nowrap"},
               {data: "modelo", className: "nowrap"},
               {data: "serie", className: "nowrap"},
               {data: "tarima", className: "nowrap"},
               {data: "estado", className: "nowrap"},
               {data: "etapa", className: "nowrap"}
           ]
              });
        /**/
        tablaDispositivos.clear().draw();
    });

  }
}
class DispositivosQR {
  constructor() {
    let url =   $("#qr-botton").data("url");
    let triage =   $("#qr-botton").data("dispositivo");
    $("#qr-botton").click( function(){
      $.ajax({
       type: "POST",
       url:url,
       data:{
         csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
         triage:triage
       },
       success:function (response){
         location.reload();

       },
       error: function (response) {
            var jsonResponse = JSON.parse(response.responseText);
             bootbox.alert(jsonResponse["mensaje"]);
        }
     });
    })

  }
}
class DispositivosTarimaList {
  constructor() {
    $("[for='id_estado']").css({"visibility":"hidden"});
    $("[for='id_etapa']").css({"visibility":"hidden"});
    $('#id_tipo').change( function() {
     var selected_tipo = $('#id_tipo option:selected').val();
    $('#dispositivo-tarima-list-form').submit(function (e) {
        e.preventDefault();
        /**/
         let tarima  = $("#id_tarima").val();
         let url = $("#qr-botton").data("url")+"?tarima="+tarima+"&tipo="+selected_tipo;
         //let url = $("#qr-botton").data("url")+"?tarima="+tarima;
         document.getElementById("qr-botton").setAttribute("href", url);
         $('#qr-botton').css({"display":"block"});
           var tablaDispositivos = $('#dispositivo-tarima-table').DataTable({
              dom: 'lfrtipB',
              destroy:true,
              buttons: ['excel', 'pdf'],
              processing: true,
              ajax: {
                  url: $('#dispositivo-tarima-list-form').attr('action'),
                  deferRender: true,
                  dataSrc: '',
                  cache: true,
                  data:function (params){
                    return {
                      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                      tarima:tarima,
                      tipo:selected_tipo,
                      estado:1,
                      etapa:1,
                    };


                  }
              },
              columns: [

                  {data: "triage", render: function(data, type, full, meta){
                    return '<a href="'+full.url+'">'+data+'</a>'
                  }},
                  {data: "tipo", className: "nowrap"},
                  {data: "marca", className: "nowrap"},
                  {data: "modelo", className: "nowrap"},
                  {data: "serie", className: "nowrap"},
                  {data: "tarima", className: "nowrap"}
              ]
            });
           /**/
           tablaDispositivos.clear().draw();
           tablaDispositivos.ajax.reload();





    });
   });


  }
}
class Prestamo {
  constructor() {
      /**/

      document.getElementById("id_fecha_inicio").disabled = true;
      var fecha = new Date();
      var dia = fecha.getDate();
      var mes = fecha.getMonth()+1;
      var year = fecha.getFullYear();
      if(dia<10){
          dia='0'+dia;
      }
      if(mes<10){
          mes='0'+mes;
      }
      var fecha = year+'-'+mes+'-'+dia;
      $('#id_fecha_inicio').text("Fecha de Inicio:"+ fecha);

  }
}
class PrestamoList {
  constructor() {
    var tabla_prestamo = $('#prestamo-table');
    var url_devolucion = $('#prestamo-table').data("devolucion");
    var acumulador = "";
    /****/
    var tabla=tabla_prestamo.DataTable({
     dom: 'lfrtipB',
     buttons: ['excel','pdf'],
     processing: true,
     ajax: {
         url: $('#prestamo-list-form').attr('action'),
         deferRender: true,
         dataSrc: '',
         cache:true,
         data: function () {
             return $('#prestamo-list-form').serializeObject(true);
         }
     },
     columns: [
       {data:"id", class:"nowrap"},
       {data:"tipo_prestamo",className:"nowrap"},
       {data:"fecha_inicio",className:"nowrap"},
       {data:"fecha_fin",className:"nowrap",
       render:function(data, type, full, meta){
         if(full.fecha_fin == null){
           return ""
         }else{
           return data
         }
       }},
       {data:"",className:"nowrap",
       render:function(data, type, full, meta){
         if(full.devuelto == true){
           return "<span class='label label-success'>Devuelto</span>"
         }else{
          return "<span class='label label-danger'>Pendiende</span>"
         }
       }},
       {data:"prestado_a",className:"nowrap"},
       {data:"cantidad",className:"nowrap"},
       {data:"", className:"nowrap", render:function(data, type, full, meta){
           return "<a target='_blank' id='dispositivo' href="+full.url_detail+" data-devolucion="+full.id+"  class='btn btn-primary'>Dispositivos</a>";
        }
      },
       {data:"", className:"nowrap", render:function(data, type, full, meta){
          if(full.devuelto == true){
            return ""
          }else{
           return "<a id='devolver' data-devolucion="+full.id+"  class='btn btn-success btn-devolver'>Devolver</a>";
          }
        }
      }
     ]

 });
 let tablabody = $('#prestamo-table tbody');
 tablabody.on('click', '.btn-devolver', function () {
           var data_fila = tabla.row($(this).parents('tr')).data();
           bootbox.confirm({
                       message: "Esta Seguro que quiere devolver este prestamo",
                       buttons: {
                           confirm: {
                               label: 'Si',
                               className: 'btn-success'
                           },
                           cancel: {
                               label: 'No',
                               className: 'btn-danger'
                           }
                       },
                       callback: function (result) {
                           if(result == true){
                             /**/
                             $.ajax({
                                 type: 'POST',
                                 url: url_devolucion,
                                 dataType: 'json',
                                 data: {
                                     csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                     prestamo:data_fila.id

                                 },
                                 success: function (response) {
                                   bootbox.alert(response.mensaje);
                                   tabla.ajax.reload();
                                 },
                                 error: function (response) {
                                      var jsonResponse = JSON.parse(response.responseText);
                                      bootbox.alert(jsonResponse["mensaje"]);
                                 }
                             });
                             /**/
                           }
                       }
                     });
       });
/***/
  $('#prestamo-list-form').submit(function (e) {
        e.preventDefault();
        tabla.clear().draw();
        tabla.ajax.reload();
    });
/****/
$("#devolver").click( function(){
  var data_fila =$("#devolver").data("devolucion");
  var url_devolucion =$("#devolver").data("urldevolucion");
  bootbox.confirm({
              message: "Esta Seguro que quiere devolver este prestamo",
              buttons: {
                  confirm: {
                      label: 'Si',
                      className: 'btn-success'
                  },
                  cancel: {
                      label: 'No',
                      className: 'btn-danger'
                  }
              },
              callback: function (result) {
                  if(result == true){
                    /**/
                    $.ajax({
                        type: 'POST',
                        url: url_devolucion,
                        dataType: 'json',
                        data: {
                            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                            prestamo:data_fila

                        },
                        success: function (response) {
                          bootbox.alert(response.mensaje);
                          tabla.ajax.reload();
                        },
                        error: function (response) {
                             var jsonResponse = JSON.parse(response.responseText);
                             bootbox.alert(jsonResponse["mensaje"]);
                        }
                    });
                    /**/
                  }
              }
            });
})
  }
}
class Desecho {
  constructor() {
    var urlDispositivo = $('#desecho-pendiente-table').data("tipo");
    var fecha = new Date();
    var dia = fecha.getDate();
    var mes = fecha.getMonth()+1;
    var year = fecha.getFullYear();
    if(dia<10){
        dia='0'+dia;
    }
    if(mes<10){
        mes='0'+mes;
    }
    var fecha = year+'-'+mes+'-'+dia;
    $('#id_fecha').val(fecha);

    var tablaDispositivo = $('#desecho-pendiente-table').DataTable({
        ajax: {
            url: urlDispositivo,
            dataType: 'json',
            dataSrc: '',
            cache: true,
            data: {
              desecho : 0
            }
        },
        columns: [
            {data: "entrada"},
            {data: "tdispositivo"},
            {data: "existencia_desecho"},
        ]
    });

  }
}

class EntradaDetalle_Dispositivo {
  constructor() {
    var tabla = $('#entradadetalle-dispositivos').DataTable({
      searching:false,
      paging:false,
      ordering:true,
      processing:true,
      destroy:true
    });
    tabla.clear().draw();

    $('#selectSubstance').select2({
      templateResult: function(data) {
          var r = data.text.split('|');
          var $result = $(
              '<div class="row">' +
                  '<div class="col-md-3">' + r[0] + '</div>' +
                  '<div class="col-md-9">' + r[1] + '</div>' +
              '</div>'
          );
          return $result;
      }
    });
  }
}
