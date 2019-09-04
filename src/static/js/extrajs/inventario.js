/*********************** ENTRADAS ************************************/
(function (AlertaEnCreacion, $, undefined) {
    AlertaEnCreacion.init = function () {
      /* -----MÉTODO DE INICIALIZACIÓN DE LA VISTA EDIT DE ENTRADA ------*/
      /* Confirma si desea finalizar la edición de la entrada, en caso de confirmar, valida y luego cierra la salida*/

        var mensaje = document.getElementById("id_en_creacion");
        var urldispositivo = $("#entrada-detalle-form").data("api");
        var primary_key = $("#entrada-detalle-form").data("key");
        $('#id_en_creacion').click(function () {
          if ($("#id_en_creacion").is(':checked')) {
            bootbox.alert({ message: "<h2>¡La Entrada vuelve a estar en desarrollo!</h2>", className:"modal modal-info fade in" });
          } else {
            bootbox.confirm({
              message: "¿Desea dar por terminada la edición de la entrada?",
              buttons: {
                confirm: {
                  label: '<i class="fa fa-check"></i> Confirmar',
                  className: 'btn-success'
                },
                cancel: {
                  label: '<i class="fa fa-times"></i> Cancelar',
                  className: 'btn-danger'
                }
              },
              callback: function (result) {
                if(result == true){
                  /*CONSUMIR API*/
                  $.ajax({
                    type: 'POST',
                    url: urldispositivo,
                    dataType: 'json',
                    data: {
                      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                      primary_key :primary_key
                    },
                    success: function (response) {
                      bootbox.alert({message: "<h2>Todo se encuentra correcto</h2>", className:"modal modal-success fade in"});
                    },
                    error: function (response) {
                      $('#id_en_creacion').iCheck('check');
                      var jsonResponse = JSON.parse(response.responseText);
                      bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + jsonResponse["mensaje"], className:"modal modal-danger fade"});
                    }
                  });
                  /*FIN DE CONSUMO*/
                } else {
                  $('#id_en_creacion').iCheck('check');
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
                                 if(full.util > 0 && full.es_kardex == "True"){
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
                   tabla_temp.tabla.ajax.reload();
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
                 tabla_temp.tabla.ajax.reload();
              },
          });

        });

        tablabody.on('click', '.btn-dispositivo', function () {
            let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
            bootbox.confirm({
                        message: "Esta seguro que desea crear estos dispositivos",
                        buttons: {
                            confirm: {
                                label: '<i class="fa fa-check"></i> Confirmar',
                                className: 'btn-success'
                            },
                            cancel: {
                                label: '<i class="fa fa-times"></i> Cancelar',
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
                              label: '<i class="fa fa-check"></i> Confirmar',
                              className: 'btn-success'
                          },
                          cancel: {
                              label: '<i class="fa fa-times"></i> Cancelar',
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
                              label: '<i class="fa fa-check"></i> Confirmar',
                              className: 'btn-success'
                          },
                          cancel: {
                              label: '<i class="fa fa-times"></i> Cancelar',
                              className: 'btn-danger'
                          }
                      },
                      callback: function (result) {
                          if(result == true){
                            /**/
                              let urldispositivo = tabla_temp.api_url + data_fila.id + "/crear_kardex/";
                              let detalle_entrada= data_fila.id
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
                error: function(response) {
                  var mensaje = JSON.parse(response.responseText)
                  bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
                }
            });
            document.getElementById("detalleForm").reset();
        });


    }

    static crear_dispositivos(urldispositivo) {
      var dialog = bootbox.dialog({
      title: 'Creacion de dispositivos ',
      message: '<p><i class="fa fa-spin fa-spinner"></i> Creando dispositivos: <b style="color:red;"></br>"Por favor espere hasta que confirme la creación de los dispositivos"<b/></p>',
      closeButton: false
        });
        $.ajax({
            type: 'POST',
            url: urldispositivo,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                $('.modal').modal('hide');
                bootbox.alert({message: "<h2>Dispositivos creados exitosamente!</h2>", className:"modal modal-success fade in",
                callback: function(result){
                   $("#entrada-table").DataTable().ajax.reload();
                  }});
            },
            error: function (response) {
              $('.modal').modal('hide');
              var mensaje = JSON.parse(response.responseText)
              bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});

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
                $('.modal').modal('hide');
                bootbox.alert({message: "<h2>Repuestos creados exitosamente!</h2>", className:"modal modal-success fade in",
                callback: function(result){
                   $("#entrada-table").DataTable().ajax.reload();
                  }});
            },
            error: function (response) {
              var mensaje = JSON.parse(response.responseText)
              bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
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
                bootbox.alert({message: "<h2>Dispositivos ingresados a Kardex!</h2>", className:"modal modal-success fade in",
                callback: function(result){
                   $("#entrada-table").DataTable().ajax.reload();
                  }});
            },
          error: function (response) {
            var mensaje = JSON.parse(response.responseText)
            bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
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
              $("#id_proveedor_kardex").attr("required", "true");
              $("#id_proveedor_kardex").removeAttr("disabled");

              $("[for='id_estado_kardex']").css({"visibility":"visible"});
              $('#id_estado_kardex').next(".select2-container").show();
              $("#id_estado_kardex").attr("required", "true");
              $("#id_estado_kardex").removeAttr("disabled");

              $("[for='id_tipo_entrada_kardex']").css({"visibility":"visible"});
              $('#id_tipo_entrada_kardex').next(".select2-container").show();
              $("#id_tipo_entrada_kardex").attr("required", "true");
              $("#id_tipo_entrada_kardex").removeAttr("disabled");
            },
            error: function (response) {
              $("[for='id_proveedor_kardex']").css({"visibility":"hidden"});
              $('#id_proveedor_kardex').next(".select2-container").hide();
              $("#id_proveedor_kardex").attr("disabled", "true");
              $("[for='id_estado_kardex']").css({"visibility":"hidden"});
              $('#id_estado_kardex').next(".select2-container").hide();
              $("id_estado_kardex").prop('disabled',true);
              $("#id_estado_kardex").attr("disabled", "true");
              $("[for='id_tipo_entrada_kardex']").css({"visibility":"hidden"});
              $('#id_tipo_entrada_kardex').next(".select2-container").hide();
              $("id_tipo_entrada_kardex").prop('disabled',true);
              $("#id_tipo_entrada_kardex").attr("disabled", "true");
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
                  if(full.tipo_entrada != "Especial"){
                    if(full.ingresado_kardex == true){
                      return "<a target='_blank' rel='noopener noreferrer' href="+full.url_kardex+" class='btn btn-success btn-ulrKardex'>Detalle</a>";
                    } else if (full.qr_dispositivo == true) {
                      return "<a target='_blank' rel='noopener noreferrer' href="+full.dispositivo_list+" class='btn btn-success'>Listado Dispositivo</a>";
                    }
                  }
                  return "";
                }},
                {data:" " ,render: function(data, type, full, meta){
                  if(full.tipo_entrada != "Especial"){
                    if(full.qr_repuestos == true){
                      return "<a target='_blank' rel='noopener noreferrer' href="+full.repuesto_list+" class='btn btn-primary'>Listado Repuestos</a>";
                    }
                  }
                  return "";
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
                bootbox.alert( "Error al crear los dispositivo:" + response.mensaje);
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
                bootbox.alert( "Error al crear los repuestos:" + response.mensaje);
            }

        });
    }
}


(function (EntradaList, $, undefined) {
  /* --- INICIALIZACIÓN DEL METODO INIT DE LA VISTA LIST DE ENTRADAS --*/
  /* Cargar el listado de entradas en base a los filtros seleccionados*/
    var tabla = $('#entrada2-table').DataTable({
        dom: 'Bfrtip',
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
            {data: "id", render: function(data, type, full, meta){
              if(full.en_creacion== "Si"){
                return "<a href="+full.urlSi+" class='btn btn-block btn-success'>"+data+"</a>";

              }else{
                return "<a href="+full.urlNo+" class='btn btn-block btn-success'>"+data+"</a>";
              }
            }},
            {data: "tipo"},
            {data: "fecha", className: "nowrap"},
            {data: "en_creacion", render: function(data, type, full, meta){
              if(full.en_creacion == 'Si'){
                return "<span class='label label-primary'>En Desarrollo</span>";
              }else{
                return "<span class='label label-danger'>Finalizada</span>";
              }
            }},
            {data: "creada_por", className: "nowrap"},
            {data: "recibida_por", className: "nowrap"},
            {data: "proveedor", className: "nowrap"},
        ]
    }).on('xhr.dt', function (e, settings, json, xhr) {
      /* Ocultar objeto de carga */
        $('#spinner').hide();
    });

    /* Inicialización de clase EntradaList*/
    EntradaList.init = function () {
        /* Al cargar la página ocultar spinner*/
        $('#spinner').hide();
        $('#entrada2-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });

        $('#entrada2-table tbody').on('click', 'button', function () {
            var data = tabla.row($(this).parents('tr')).data();
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
                    message: "¿Está seguro que quiere rechazar este detalle de desecho?",
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
                        if (result == true) {
                          /**/
                          bootbox.prompt({
                            title: "¿Por que rechazo este detalle?",
                            inputType: 'textarea',
                            callback: function (result) {
                                console.log(result);
                                $.ajax({
                                  type: "POST",
                                  url: urlRechazar,
                                  dataType: 'json',
                                  data: {
                                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                    detalle:data_fila.id,
                                    comentario:result
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
                        });
                          /**/
                          
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
                                  label: 'Si',
                                  className: 'btn-success'
                              },
                              cancel: {
                                  label: 'No',
                                  className: 'btn-danger'
                              }
                          },
                          callback: function (result) {
                            /**/
                            bootbox.prompt({
                              title: "¿Por que rechazo este dipositivo?",
                              inputType: 'textarea',
                              callback: function (result) {                                  
                                  $.ajax({
                                    type: "POST",
                                    url: urlRechazarDispositivo,
                                    dataType: 'json',
                                    data: {
                                      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                      detalle:data_fila.id,
                                      comentario:result
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
                            /**/
                         


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
                                    data_result.push('<option value='+data[i].id + ' data-tipo="'+data[i].descripcion+'" data-cantidad="'+cantidad+'">'+data[i].entrada+'</option>');
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
                        label: 'Si',
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
            message: "¿Está seguro que quiere recibir esta solicitud de movimiento?",
            buttons: {
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirmar',
                    className: 'btn-success'
                },
                cancel: {
                    label: '<i class="fa fa-times"></i> Cancelar',
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
            message: "¿Está seguro de aprobar esta petición de dispositivos?",
            buttons: {
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirmar',
                    className: 'btn-success'
                },
                cancel: {
                    label: '<i class="fa fa-times"></i> Denegar',
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
                        //
                        bootbox.confirm({
                            className:"modal modal-info fade in",
                            message: "<h3>La Existencia del Dispositivo es de: </h3><h2>" + response['existencia'] + "</h2>",
                            buttons: {
                                confirm: {
                                    label: '<i class="fa fa-check"></i> Entendido',
                                    className: 'btn-success'
                                },
                            },
                            callback: function (result) {
                                if (result == true) {
                                    location.reload();
                                }
                            }
                        });
                        //

                      },
                  });
                }
            }
        });
    });

    $('#recibido-kardex').click(function (e) {
       e.preventDefault();
        bootbox.confirm({
            message: "¿Esta seguro que desea rechazar estos dispositivos?",
            buttons: {
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirmar',
                    className: 'btn-success'
                },
                cancel: {
                    label: '<i class="fa fa-times"></i> Cancelar',
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

class SolicitudMovimientoValidar {
  constructor() {
    var tipo_dispositivo;
    $('#tipo_dispositivo_movimiento').change( function() {      
      tipo_dispositivo=$('#tipo_dispositivo_movimiento option:selected').text();
      $.ajax({
          type: "POST",
          async:false,
          url: $('#solicitud').data('url'),
          dataType: 'json',
          data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            tipo_dispositivo: tipo_dispositivo,
          },
          success: function (response) {
            var disponibles = response['mensaje'];
            $("[for='cantidad']").text(disponibles);
            $("#existencia-head").css({"display":"block"});
          },
          error:function(response){
            var jsonResponse = JSON.parse(response.responseText);
            bootbox.alert(jsonResponse.mensaje);
            location.reload();
          },
      });

    });

    $('#id_tipo_dispositivo').change( function() {      
      tipo_dispositivo=$('#id_tipo_dispositivo option:selected').text();
      var no_salida=$('#id_no_salida option:selected').val();
      $.ajax({
          type: "POST",
          async:false,
          url: $('#solicitud').data('devolucion'),
          dataType: 'json',
          data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            tipo_dispositivo: tipo_dispositivo,
            no_salida: no_salida,
          },
          success: function (response) {
            var disponibles = response['mensaje'];
            $("[for='cantidad']").text(disponibles);
            $("#existencia-head").css({"display":"block"});
          },
          error:function(response){
            var jsonResponse = JSON.parse(response.responseText);
            bootbox.alert(jsonResponse.mensaje);
            location.reload();
          },
      });

    });
    $("#existencia-head").css({"display":"none"});
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
        let cantidad_disponible = $("#solicitud-table").data("dispo");
        let cantidad_asignar = cantidad-cantidad_disponible;        
        $('#id_dispositivos').val("").trigger('change');
        var lista_triage = [];
        sel_dispositivos.select2({
            maximumSelectionLength : cantidad_asignar,
            placeholder: "Ingrese los triage",
            width : '50%'
        });
        let cantidad_dispositivos = sel_dispositivos;
        $('form').on('submit', function(e){           
           let restante  = cantidad_dispositivos.select2('data').length - cantidad_asignar;           
          if(cantidad_dispositivos.select2('data').length > cantidad_asignar){
            bootbox.alert({ message: "<h3>Ya no puede ingresar mas dispositivos , tiene de excendente: "+restante+"!</h3>", className:"modal modal-danger fade in" });
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
                           maximumSelectionLength : cantidad_asignar,
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
                      bootbox.alert({message: "<h3>Este dispositivo no esta disponible</h3>", className:"modal modal-danger fade in"});
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
              maximumSelectionLength : ccantidad_asignar,
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
                  bootbox.alert("Paquete y Dispositivos aprobados");
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
    var validar = $('#revicion_add').data('validar');
    if(validar == 1){
      var nueva_url =api_url_revision+"?estado=1";
    }else{
      var nueva_url =api_url_revision+"?aprobada=false"
    }; 
    var tablaRevision = revision_tabla.DataTable({
      processing:true,
      retrieve:true,
      ajax:{        
        url:nueva_url,
        dataSrc:'',
        cache:false,
        deferRender:true,
        processing:true,
      },
      columns:[
        {data:"salida", render: function( data, type, full, meta){
          return '<a href="'+full.urlSalida+'">'+full.no_salida+'</a>'
        }},
        {data:"escuela", render: function( data, type, full, meta){          
        if(full.escuela===undefined){
          return "";
        }else{
          return '<a target=_blank  href="'+full.escuela_url+'">'+full.escuela+'</a>'
        }
          
        }},
        {data:"beneficiario"},
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
    /**/
     var tipo_garantia = $("#salidas-paquete-table").data("garantia");     
     if(tipo_garantia =="Garantia"){
      $("[for='id_cooperante']").css({"visibility":"hidden"});      
      $('#id_cooperante').next(".select2-container").hide(); 
     };
     /**/
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
    var url_paquetes = $("#salidas-paquete-table").data("urlpaquetes");
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
    $("[for='id_garantia']").css({"visibility":"hidden"});
    $("[for='id_beneficiario']").css({"visibility":"hidden"});
    $('#id_garantia').next(".select2-container").hide();
    $('#id_beneficiario').next(".select2-container").hide();  
    $('#salidaform').on('submit', function(e){
      var udi = $("#id_udi").val();
      var beneficiario = $("#id_beneficiario").val(); 
    });
    $('#salidas-table').DataTable({
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      "order": [[ 3, "desc" ]],
      ajax:{
        url:url_salida,
        dataSrc:'',
        cache:true,

      },
      columns:[
        {data: "no_salida", render: function(data, type, full, meta){
          if(full.estado == 'Entregado'){
            return "<a target='_blank' rel='noopener noreferrer' href="+full.detail_url+" class='btn btn-success'>"+data+"</a>";
          }else{
            return "<a target='_blank' rel='noopener noreferrer' href="+full.url+" class='btn btn-success'>"+data+"</a>";
          }
        }},
        {data:"id"},
        {data:"tipo_salida"},
        {data:"fecha"},
        {data: "estado", render: function(data, type, full, meta){
          if(full.estado == 'Pendiente'){
            return "<span class='label label-danger'>En Desarrollo</span>";
          }else if(full.estado == 'Listo'){
            return "<span class='label label-primary'>Listo</span>";
          } else {
            return "<span class='label label-success'>Entregado</span>";
          }
        }},
        {data:"escuela", render: function(data, type, full, meta){
          if(full.escuela===undefined){
            return " ";
          }else{
            return "<a href="+full.escuela_url+">"+full.escuela+"</a>";
          }

        }},
        {data:"beneficiario"},
      ]
    });
    /* */
    $('#salida-list-form').submit(function (e) {
          e.preventDefault();
        $('#salidas-table').DataTable({
          dom: 'Bfrtip',
          destroy:true,
          buttons: ['excel', 'pdf', 'copy'],          
          ajax:{
            url:$('#salida-list-form').attr('action'),
            dataSrc:'',
            cache:true,
            data: function (params) {
              return $('#salida-list-form').serializeObject(true);
          }

          },
          columns:[
            {data: "no_salida", render: function(data, type, full, meta){
              if(full.estado == 'Entregado'){
                return "<a target='_blank' rel='noopener noreferrer' href="+full.detail_url+" class='btn btn-success'>"+data+"</a>";
              }else{
                return "<a target='_blank' rel='noopener noreferrer' href="+full.url+" class='btn btn-success'>"+data+"</a>";
              }
            }},
            {data:"id"},
            {data:"tipo_salida"},
            {data:"fecha"},
            {data: "estado", render: function(data, type, full, meta){
              if(full.estado == 'Pendiente'){
                return "<span class='label label-danger'>En Desarrollo</span>";
              }else if(full.estado == 'Listo'){
                return "<span class='label label-primary'>Listo</span>";
              } else {
                return "<span class='label label-success'>Entregado</span>";
              }
            }},
            {data:"escuela", render: function(data, type, full, meta){
              if(full.escuela===undefined){
                return " ";
              }else{
                return "<a href="+full.escuela_url+">"+full.escuela+"</a>";
              }

            }},
            {data:"beneficiario"},
          ]
        });
    });
    /* */
    var nueva_tabla = tabla_paquetes.DataTable({
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
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
          if(full.aprobado == true && full.aprobado_kardex==true){
         
            return "<span class='label label-success'>Revisado</span>"

          }else{
            if(full.aprobado_kardex==true){
              return "<span class='label label-warning'>Revisado CC</span>"
            }else{
              return "<span class='label label-danger'>No Revisado</span>"
            }
            
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
                if(full.aprobado_kardex == true){
                  return " ";
                }else{
                  return "<a id='conta-aprobar'  class='btn btn-success btn-aprobar-conta'>Aprobar</a>";
                }

              }
            }else{
              return "<a target='_blank' rel='noopener noreferrer' href="+full.url_detail+" class='btn btn-success'>Ver Dispositivos</a>";
            }

          }
        }},
        {data:"", render: function(data, type, full, meta){
          if(full.aprobado ==false){
            if(full.usa_triage == "False"){
              if(full.aprobado_kardex == true){
                return " ";
              }else{
                  return "<a id='conta-rechazar'  class='btn btn-warning btn-rechazar-conta'>Rechazar</a>";
              }


            }else{
              return "<a target='_blank' rel='noopener noreferrer' href="+full.urlPaquet+" class='btn btn-primary btn-asignar'>Asignar Dispositivos</a>";
            }

          }else{
            return "";
          }

        }}
      ]
    });
    /**Asignar Dispositivos**/
    nueva_tabla.on('click','.btn-asignar', function () {
      location.reload();
    } );

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
            bootbox.alert("Paquete aprobado");
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
                                         bootbox.alert("Salida Aprobada");
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
            tipo_dispositivo:tipo_paquete,
            salida:salida_pk,
          },
          success: function (response){
            $('#id_cantidad').val(parseInt(response['mensaje']));
            $("#label_kardex").css({"visibility":"visible"});
            $('#existencia_kardex').html("<b>"+response['mensaje']);
            disponible = parseInt(response['mensaje']);
            
            if(disponible <= 0){
              $('#paquetes_add').css({"visibility":"hidden"});
            } else {
              $('#paquetes_add').css({"visibility":"visible"});
            }

            /*if(response['mensaje']=="Usa Triage"){
                $('#id_cantidad').val("");
                dispositivo_triage =1;
                $("#label_kardex").css({"visibility":"hidden"});
                $('#existencia_kardex').html(" ");
            }else{
              $('#id_cantidad').val("");
              $("#label_kardex").css({"visibility":"visible"});
               $('#existencia_kardex').html("<b>"+response['mensaje']);
               disponible = parseInt(response['mensaje']);
            }*/
          },
          error:function(error){
            var jsonResponse = JSON.parse(error.responseText);
            bootbox.alert(jsonResponse["mensaje"]);
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
        if(cantidad > disponible || disponible <= 0){
          $('#paquetes_add').css({"visibility":"hidden"});
          $('#id_cantidad').val("");
          bootbox.alert("No has dipositivos suficientes para asignar");
        }else{
           $('#paquetes_add').css({"visibility":"visible"});
        }
      }

    });
    /**/
    /* MOSTRAR PAQUETES VÁLIDOS */
    $('#id_tipo_paquete').select2("destroy");
    var data_result = []
    $.ajax({
      type: "POST",
      url: url_paquetes,
      data:{
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        salida:salida_pk,
      },
      error:function(error){
        console.log("Error");
      },
      success: function (data){
        $('#id_tipo_paquete').empty();
        data_result.push('<optgroup class="def-cursor" label="Tipo" data-cantidad="Existencia">')
        data_result.push('<option value="" data-cantidad="">-------</option>');
        for (var i in data){
          var cantidad = data[i].existencia
          data_result.push('<option value='+data[i].id + ' data-cantidad="'+cantidad+'">'+data[i].nombre+'</option>');
        }
        data_result.push('</optgroup>')
        $('#id_tipo_paquete').append(data_result);
      },
    });
    $('#id_tipo_paquete').select2({
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
        var cantidad = $(data.element).data('cantidad');
        var classAttr = $(data.element).attr('class');
        var hasClass = typeof classAttr != 'undefined';
        classAttr = hasClass ? ' ' + classAttr : '';
        var $result = $(
          '<div class="row">' +
          '<div class="col-md-7 col-xs-6' + classAttr + '">' + data.text + '</div>' +
          '<div class="col-md-2 col-xs-6' + classAttr + '">' + cantidad + '</div>' +
          '</div>');
        return $result;
      },
      templateSelection: function (data) {
        if(!data.id) { return data.text }
        var cantidad = $(data.element).data('cantidad');
        var result = data.text
        return result
      }
    }).on('select2:select', function (e) {
      if (e.params.data.text != '') {
        var id = $(this).attr('id');
        var select2 = $("span[aria-labelledby=select2-" + id + "-container]");
        select2.removeAttr('style');
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
        $("[for='id_udi']").css({"visibility":"hidden"});
        $("#id_udi").attr('type','hidden');
        $("#id_udi").val("");
        $("#id_beneficiario").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"visible"});
        $('#id_beneficiario').next(".select2-container").show();
        $("[for='id_garantia']").css({"visibility":"hidden"});
        $('#id_garantia').next(".select2-container").hide();
        /**/
        $("[for='id_cooperante']").css({"visibility":"hidden"});      
        $('#id_cooperante').next(".select2-container").hide(); 
      }else if(tipoSalida == 4 || tipoSalidaText =='A terceros') {
        $("[for='id_entrega']").css({"visibility":"hidden"});
        $("#id_entrega").css({"visibility":"hidden"});
        $("#id_entrega").prop('checked',false);
        /**/
        $("#id_udi").attr('type','hidden');
        $("[for='id_udi']").css({"visibility":"hidden"});
        $("[for='id_beneficiario']").css({"visibility":"visible"});
        $("#id_beneficiario").css({"visibility":"visible"});
        $("#id_udi").val(" ");
        $('#id_beneficiario').next(".select2-container").show();
        $("[for='id_garantia']").css({"visibility":"hidden"});
        $('#id_garantia').next(".select2-container").hide();
        /**/
        $("[for='id_cooperante']").css({"visibility":"hidden"});      
        $('#id_cooperante').next(".select2-container").hide(); 
        /**/
        $("#id_udi").val("");       
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
         /**/
         $("[for='id_cooperante']").css({"visibility":"hidden"});      
         $('#id_cooperante').next(".select2-container").hide();
         /* */
         $("#id_beneficiario").val(" ");
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
        /**/
        $("[for='id_cooperante']").css({"visibility":"visible"});      
        $('#id_cooperante').next(".select2-container").show();
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
    let urlredireccion = $('#paquetes-revision').data('redirect');
    let urlraprobar = $('#paquetes-revision').data('urlaprobar');
    let urlrechazar = $('#paquetes-revision').data('urlrechazar');
    var api_paquete_salida= $('#paquetes-revision').data('id');
    let api_aprobar_salida=$('#aprobar-btn').data('url');
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
                var triage = $("#area_scanner").val();
                var mensaje = JSON.parse(triage);
                 /*Api*/
                $.ajax({
                  type: "POST",
                  url: urlraprobar,
                  data:{
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                    triage:mensaje.triage,
                    tipo:mensaje.tipo,
                    kardex:false,
                    salida:api_paquete_salida
                  },
                  success: function (response){
                      if(response.code == 1){
                        bootbox.alert(response.mensaje, function (){
                          location.reload();
                        });
                      }else{
                       bootbox.alert("El dispositivo ha sido aprobado");
                       $("#area_scanner").focus();
                       location.reload();

                      }
                  },
                  error: function (response) {
                      var jsonResponse = JSON.parse(response.responseText);
                      bootbox.alert(jsonResponse["mensaje"]);
                  }
                });
                 /**/
            }
          $("#area_scanner").val("");
          $("#area_scanner").focus();
        }

        /*Fin scanner*/

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
          triage:data_fila.dispositivo,
          tipo:data_fila.tipo,
          kardex:false,
          salida:api_paquete_salida
        },
        success: function (response){
            bootbox.alert("Dispositivos aprobados");
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
                 triage:data_fila.dispositivo,
                 kardex:false
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
      bootbox.alert("Error al crear datos");
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
       message: "¿Esta  seguro que desea aprobar esta revicion de salida?",
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
                 bootbox.alert("¡Felicidades! " + response.usuario + " " + response.mensaje ,function (){
                   $("#aprobar-btn").css({"visibility":"hidden"});
                    window.location= urlredireccion;
                 });
             },
             error: function (response) {
                  var jsonResponse = JSON.parse(response.responseText);
                  bootbox.alert(jsonResponse.mensaje);

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
        {data:"cantidad"},
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
        {data:"cantidad"},
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
            bootbox.alert("Paquete aprobado");
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
                   title: "Por qué rechazo este dispositivo?",
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
    var tablabodyRechazar = $("#rechazar-dispositivo tbody tr");
    var urlCambio = $("#rechazar-dispositivo").data('url');
    var urlAprobar = $("#rechazar-dispositivo").data('urlaprobar');
    var urlAprobarControl = $("#rechazar-dispositivo").data('urlaprobar');
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
                 var id_comentario = $("#rechazar-dispositivo").data('id');
                 var url = $("#rechazar-dispositivo").data('urlhistorico');
                 bootbox.prompt({
                   title: "Por que rechazo este dispositivo?",
                   inputType: 'textarea',
                   callback: function (result) {
                     if (result) {
                       crear_historial_salidas_cc(url, id_comentario, result);
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
      var tipo = $(this).data("tipo");
      let data_triage = $(this).attr("data-triage");
      var data_paquete=$(this).attr("data-paquete");
      var data_idpaquete=$(this).attr("data-idpaquete");
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
                 tipo:tipo,
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
    var crear_historial_salidas_cc = function(url, id_comentario, comentario){
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
      bootbox.alert("Error al crear datos");
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
      let restante = cantidad_dispositivos.select2('data').length - cantidad_asignar ;
     if(cantidad_dispositivos.select2('data').length > cantidad_asignar){
        bootbox.alert("Ya no puede ingresar mas dispositivos , tiene de excendente:"+restante);
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
                         maximumSelectionLength : cantidad_asignar,
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
    /****/
    //Scanner  aprobar dispositivo paquete
    var inputStartAprobar, inputStopAprobar, firstKeyAprobar, lastKeyAprobar, timingAprobar, userFinishedEnteringAprobar;
    var minCharsAprobar = 3;

    // handle a key value being entered by either keyboard or scanner
    $("#area_scanner_aprobar").keypress(function (e) {
        // restart the timer
        if (timingAprobar) {
            clearTimeout(timingAprobar);
        }

        // handle the key event
        if (e.which == 13) {
            // Enter key was entered

            // don't submit the form
            e.preventDefault();

            // has the user finished entering manually?
            if ($("#area_scanner_aprobar").val().length >= minCharsAprobar){
                userFinishedEnteringAprobar = true; // incase the user pressed the enter key
                inputCompleteAprobar();
            }
        }
        else {
            // some other key value was entered

            // could be the last character
            inputStopAprobar = performance.now();
            lastKeyAprobar = e.which;
            // don't assume it's finished just yet
            userFinishedEnteringAprobar = false;

            // is this the first character?
            if (!inputStartAprobar) {
                firstKeyAprobar = e.which;
                inputStartAprobar = inputStopAprobar;

                // watch for a loss of focus
                $("body").on("blur", "#area_scanner_aprobar", inputBlurAprobar);
            }

            // start the timer again
            timingAprobar = setTimeout(inputTimeoutHandler, 500);
        }
    });

    // Assume that a loss of focus means the value has finished being entered
    function inputBlurAprobar(){
        clearTimeout(timingAprobar);
        if ($("#area_scanner_aprobar").val().length >= minCharsAprobar){
            userFinishedEnteringAprobar = true;
            inputCompleteAprobar();
        }
    };


    // reset the page
    $("#reset").click(function (e) {
        e.preventDefault();
        resetValuesAprobar();
    });

    function resetValuesAprobar() {
        // clear the variables
        inputStartAprobar = null;
        inputStopAprobar = null;
        firstKeyAprobar = null;
        lastKeyAprobar = null;
        // clear the results
        inputCompleteAprobar();
    }

    // Assume that it is from the scanner if it was entered really fast
    function isScannerInputAprobar() {
        return (((inputStopAprobar - inputStartAprobar) / $("#area_scanner_aprobar").val().length) < 15);
    }

    // Determine if the user is just typing slowly
    function isuserFinishedEnteringAprobar(){
        return !isScannerInputAprobar() && userFinishedEnteringAprobar;
    }

    function inputTimeoutHandler(){
        // stop listening for a timer event
        clearTimeout(timingAprobar);
        // if the value is being entered manually and hasn't finished being entered
        if (!isuserFinishedEnteringAprobar() || $("#area_scanner_aprobar").val().length < 3) {
            // keep waiting for input
            return;
        }
        else{
            reportValuesAprobar();
        }
    }

    // here we decide what to do now that we know a value has been completely entered
    function inputCompleteAprobar(){
        // stop listening for the input to lose focus
        $("body").off("blur", "#area_scanner_aprobar", inputBlurAprobar);
        // report the results
        reportValuesAprobar();
    }

    function reportValuesAprobar() {
        var inputMethod = isScannerInputAprobar() ? "Scanner" : "Keyboard";
        if(inputMethod == "Scanner"){
            var triage = $("#area_scanner_aprobar").val();
            var mensaje = JSON.parse(triage);
             /*Api*/
             $.ajax({
               type: "POST",
               url: urlAprobarControl,
               dataType: 'json',
               data:{
                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                 triage:mensaje.triage,
                 tipo:mensaje.tipo,
                 paquete:$('#rechazar-dispositivo').data('paquete'),
                 idpaquete:$('#rechazar-dispositivo').data('idpaquete')
               },
               success: function (response){
                 bootbox.alert(response.mensaje);
                 $("#area_scanner_aprobar").focus();
                  location.reload();
               },
               error: function (response){
                var jsonResponse = JSON.parse(response.responseText);             
                /**/               
                    bootbox.confirm({
                          message:jsonResponse["mensaje"] ,
                          buttons: {
                              confirm: {
                                  label: 'Ok',
                                  className: 'btn-danger'
                              }
                          },
                          callback: function (result) {
                            if(result){
                                location.reload();
                            }else{
                                location.reload();
                            };
                          }
                      });
                /**/
               }
             });
             /**/
        }
    }
    $("#area_scanner_aprobar").val("");
    $("#area_scanner_aprobar").focus();

    //Fin Scanner aprobar dispositivo paquete
    /*Editar Cantidad de Dispositivos */
    $("#editar_cantidad").click(function (e) {
      bootbox.prompt("Ingrese la cantidad nueva", function(result){ 
        var nueva_cantidad = result;
        console.log(result); 
        console.log($("#editar_cantidad").data("cantidaurl"));
        if(result<cantidad){
          bootbox.alert("Cantidad no disponible tiene que ser mayor a la cantidad del paquete");
        }else{
          /* */
          $.ajax({
            type: "POST",
            url: $("#editar_cantidad").data("cantidaurl") ,
            dataType: 'json',
            data:{
              csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),              
              cantidad:nueva_cantidad,  
              idpaquete:$("#editar_cantidad").data("nuevoid")
            },
            success: function (response){
              bootbox.alert(response.mensaje);
               location.reload();
            },
            error: function (response){    
              console.log(response);        
              //bootbox.alert(response.responseText);
            }
          });
          /* */
        };
    });
  });

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
              if(full.estado=="Utilizado"){
                return "";
              }else{
                return "<button  id='button-repuesto' class='btn btn-info repuesto-btn'>Asignar</button>";
              }
             
            }
          }},
          {data:"",className:"nowrap", render:function(data, type, full, meta){
            return "<button  id='button-finalizar-repuesto' class='btn btn-danger repuesto-terminar-btn'>Terminar</button>";
          }}
        ]
      });

      tabla.clear().draw();
      tabla.ajax.reload();

      tabla.on('click','.repuesto-btn',function () {
        let repuesto = tabla.row($(this).parents('tr')).data();
        bootbox.prompt({
          title: "Ingrese el triage del dispositivo", 
          centerVertical: true,
          callback: function(result){               
              if(result==null){
                bootbox.alert("por favor ingrese un triage valido");
              }else{                
               var triage_asignar_repuesto = result;
                /**/
                bootbox.prompt({
                  title: "Comentario para este repuesto",
                  inputType: 'textarea',
                  callback: function (result) {
                    console.log(triage_asignar_repuesto);  
                    console.log(result);
                    $.ajax({
                      type: "POST",
                      url:url_repuestos +"asignar_repuesto/",
                      data:{
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                        repuesto:repuesto.id,
                        triage:triage_asignar_repuesto,
                        comentario:result
                      },
                      success:function (response){
                        if(response.codigo=1){
                          bootbox.alert("El dispositivo no existe por favor ingrese otro");
                        }else{
                          tabla.ajax.reload();
                        }
                        
                      },
                      error: function (response) {
                        var jsonResponse = JSON.parse(response.responseText);
                         bootbox.alert(jsonResponse["mensaje"]);
                    }
                    });                      
                  }
                });
                /**/
              }
          }
        });        
      });
      /* */
      tabla.on('click','.repuesto-terminar-btn',function () {
        let repuesto = tabla.row($(this).parents('tr')).data();       
         bootbox.confirm({
          message: "¿Desea finalizar  la asignacion de este repuesto?",
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
                  url:url_repuestos +"terminar_repuesto/",
                  data:{
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                    repuesto:repuesto.id,                    
                  },
                  success:function (response){
                    tabla.ajax.reload();
                  }
                });
              }
          }
      });
      });
      /* */
    });
  }
}
class DispositivoList {
  constructor() {
      $('#dispositivo-list-form').submit(function (e) {
          e.preventDefault();
          /**/
          var tablaDispositivos = $('#dispositivo-table-search').DataTable({
             dom: 'lfrtipB',
             destroy:true,
             buttons: ['excel', 'pdf'],
             processing: true,
             deferLoading: [0],
             ajax: {
                 url: $('#dispositivo-list-form').attr('action'),
                 deferRender: true,
                 dataSrc: '',
                 cache: true,
                 data: function (params) {
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
      $('#id_fecha_inicio').text(fecha);

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
       {data:"fecha_estimada",className:"nowrap",
       render:function(data, type, full, meta){
         if(full.fecha_fin == null){
           return data
         }else{
           return ""
         }
       }},
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
     ],
     "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
        var today = new Date();
        if ( aData[2] == "5" )
        {
          $('td', nRow).css('background-color', 'Red');
        }
        else if ( aData[2] == "4" )
        {
          $('td', nRow).css('background-color', 'Orange');
        }
      }

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
            {data: "descripcion"},
            {data: "existencia_desecho"},
            {data: "fecha_desecho"},
        ]
    });

  }
}

class DesechoList{
  constructor(){
    $('#desecho-list-form').submit(function (e) {
      e.preventDefault();
      
    $('#desecho-list-table').DataTable({
      dom: 'Bfrtip',
      destroy:true,
      buttons: ['excel', 'pdf', 'copy'],          
      ajax:{
        url:$('#desecho-list-form').attr('action'),
        dataSrc:'',
        cache:true,
        data: function (params) {
          return $('#desecho-list-form').serializeObject(true);
      }

      },
      columns:[       
        {data:"id", render: function(data, type, full, meta){
          if(full.en_creacion==true){            
            return "<a href="+full.url_edit+">"+full.id+"</a>"; 
          }else{           
            return "<a href="+full.url_detalle+">"+full.id+"</a>"; 
          }
        }},        
        {data:"fecha"},
        {data:"empresa"},
        {data: "en_creacion", render: function(data, type, full, meta){        
          if(full.en_creacion==true){
            return "<span class='label label-danger'>Pendiente</span>";
            
          }else{
            return "<span class='label label-success'>Entregado</span>";
          }
          
        }}, 
      ]
    });
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

(function (MovimientoList, $, undefined) {
      var tablaDispositivos = $('#movimiento-list-table').DataTable({
        dom: 'lfrtipB',
        destroy:true,
        buttons: ['excel', 'pdf'],
        processing: true,
        deferLoading: [0],
        ajax: {
            url: $('#movimiento-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            cache: true,
            data: function (params) {
                return $('#movimiento-list-form').serializeObject(true);
            }
        },
        columns: [            
            {data: "id", className: "nowrap", render: function(data, type, full, meta){
              return "<a href="+full.url+">"+full.id+"</a>";
            }},
            {data: "no_salida", className: "nowrap", render: function(data, type, full, meta){
              if(full.no_salida ==null){
                return ""
              } else {
                return "<a href="+full.url_salida+">"+full.no_salida_str+"</a>";
              }
            }},
            {data: "fecha_creacion", className: "nowrap"},
            {data: "tipo_dispositivo", className: "nowrap"},
            {data: "cantidad", className: "nowrap"},
            {data: "creada_por", className: "nowrap"},
            {data: "autorizada_por", className: "nowrap", render: function(data, type, full, meta){               
             if(full.autorizada_por==null){
              return "";
             }else{
              return full.autorizada_por;
             }

           }},
            {data: "devolucion", className: "nowrap", render: function(data, type, full, meta){
              if(full.devolucion==true){
               return "<span class='label label-danger'>Devolucion</span>";
              }else{
               return "<span class='label label-primary'>Solicitud</span>";
              }

            }},
            {data: "desecho", className: "nowrap", render: function(data, type, full, meta){
             if(full.desecho===true){
              return "<input type='checkbox' name='desecho' class='icheckbox_square-red' disabled   checked/>";
             }else{
              return "";
             }

           }},
            {data: "terminada", className: "nowrap", render: function(data, type, full, meta){
             if(full.rechazar===true){
              return " <span class='label label-danger'>RECHAZADA</span>";
             }else{
              if(full.recibida==true){
               return " <span class='label label-success'>Recibido</span>";
              }else{
                if(full.terminada===true){
                 return " <span class='label label-warning'>Entregado</span>"
                }else{
                  return "<span class='label label-danger'>Pendiente</span>"
                }
              }
             }

           }}
        ]
      }).on('xhr.dt', function (e, settings, json, xhr) {
      /* Ocultar objeto de carga */
        $('#spinner').hide();
    });

      /* Inicialización de clase EntradaList*/
    MovimientoList.init = function () {
        /* Al cargar la página ocultar spinner*/
        $('#spinner').hide();
        $('#movimiento-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tablaDispositivos.clear().draw();
            tablaDispositivos.ajax.reload();
        });

        $('#movimiento-list-table tbody').on('click', 'button', function () {
            var data = tabla.row($(this).parents('tr')).data();
        });

    }
}(window.MovimientoList = window.MovimientoList || {}, jQuery));