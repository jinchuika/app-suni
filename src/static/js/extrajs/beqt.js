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
      if(selected_tipo == 'Compra' || selected_tipo == 'BEQT' ){
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
          //let urldispositivo = tabla_temp.api_url + key + "/validar_kardex/";
         // let tipo_dispositivo=$('#id_tipo_dispositivo option:selected').val();
          //EntradaUpdate.validar_kardex(urldispositivo, tipo_dispositivo);
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
                {data: "descripcion"},                
                {data: "total"},
                {data: "precio_unitario"},
                {data: "precio_total"},
                {data: "creado_por"},
                {data: "",render: function(data, type, full, meta){                 
                  if(full.pendiente_autorizar == false){
                     return "	<span class='label label-danger'>Pendiente</span>";
                  }else{
                    if(full.autorizado == false){
                        return "	<span class='label label-warning'>Revisado</span>";
                    }else{
                        return "	<span class='label label-success'>Autorizado</span>";
                    }

                  }

                }},
                {
                    data: "",render: function(data, type, full, meta){                     
                      if(full.grupos == 4){
                        if(full.autorizado == true){
                          return "";
                        }else{
                          if(full.dispositivos_creados == true){
                              if(full.usa_triage == "False"){                               
                                  var total_detalle_editar = full.util;
                                  if (total_detalle_editar != full.total){
                                    return "<a href="+full.update_url+" class='btn btn-info btn-editar'>Editar</a>";
                                  }else{
                                    return "";
                                  }

                              
                              }else{
                                  return "";
                              }
                          }else{
                            var total_detalle_editar_normal = full.util;
                            if(total_detalle_editar_normal != full.total){
                              return "<a href="+full.update_url+" class='btn btn-info btn-editar'>Editar</a>";
                            }else{
                              return "";
                            }

                          }
                        }

                      }else{
                        if(full.grupos ==  20){
                          if(full.pendiente_autorizar == true){
                            if (full.autorizado == false){
                                return "<a  class='btn btn-info btn-autorizar'>Autorizar</a>";
                            }else{
                              return "";
                            }

                        }else{
                          return "";
                        }
                        }else{
                          if(full.pendiente_autorizar == false){
                            return "<a  class='btn btn-info btn-aprobar'>Aprobar</a>";
                          }else{
                            return "";
                          }

                        }
                      }

                    }
                },
                {
                    data: "", render: function(data, type, full, meta){
                      if (full.grupos == 4){
                        if(full.tipo_entrada != "Especial"){
                            if(full.dispositivos_creados == false){
                              if(full.usa_triage == "True" && full.total >= 1){
                                if(full.autorizado !=false){
                                  return "<button class='btn btn-primary btn-dispositivo'>Crear Disp</button>";
                                }else{
                                  return "";
                                }

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
                                console.log("url dipositivo:" + urldispositivo)
                                EntradaUpdate.crear_dispositivos(urldispositivo);
                            }
                        }
                      });
        });        
        /*Botones para  autorizar y aprobar la revison de los dispositivos*/
        tablabody.on('click', '.btn-aprobar', function () {
           let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
           EntradaUpdate.validar_detalles(tabla_temp.api_url,data_fila.id,data_fila.autorizado,data_fila.pendiente_autorizar);

        });
        tablabody.on('click', '.btn-autorizar', function () {
           let data_fila = tabla_temp.tabla.row($(this).parents('tr')).data();
           EntradaUpdate.validar_detalles(tabla_temp.api_url,data_fila.id,data_fila.autorizado,data_fila.pendiente_autorizar);

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

    static validar_detalles(urldetalles, id, autorizado, pendiente_autorizar) {
      $.ajax({
            type: "post",
            url: urldetalles+"autorizar_detalles/",
            dataType: 'json',
            data: {
              csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
              id:id,
              autorizado:autorizado,
              pendiente_autorizar:pendiente_autorizar,
            },
            success: function (response) {
              $("#entrada-table").DataTable().ajax.reload();
               console.log("Abrir");

            },
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
            new BuscadorTabla();
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