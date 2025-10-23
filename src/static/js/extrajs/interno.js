class InventarioInterno {
  constructor () {
   /**/
   var url_interno = $("#interno-table").data("url");
   var url_devolver = $("#interno-table").data("urldevolver");
   /**/
    var tabla = $('#interno-table').DataTable({
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      "order": [[4, "desc"]],
      ajax:{
        url: url_interno,
        dataSrc:'',
        cache:true,
      },
      columns:[
        {data: "no_asignacion", render: function(data, type, full, meta){
          if(full.estado == 'Asignado'){
            return "<a target='_blank' rel='noopener noreferrer' href="+full.detail_url+" class='btn btn-success'>"+data+"</a>";
          }else{
            return "<a target='_blank' rel='noopener noreferrer' href="+full.url+" class='btn btn-success'>"+data+"</a>";
          }
        }},
        {data:"colaborador_asignado"},
        {data:"fecha_asignacion"},
        {data:"fecha_devolucion", render: function(data, type, full, meta){
         var newDate = new Date(full.fecha_devolucion);
         return newDate.getFullYear()+'-' + (newDate.getMonth()+1) + '-'+newDate.getDate();
        }},
        {data: "estado", render: function(data, type, full, meta){
          if(full.estado == 'Borrador'){
            return "<span class='label label-danger'>Borrador</span>";
          }else if(full.estado == 'Asignado'){
            return "<span class='label label-warning'>Asignado</span>";
          } else {
            return "<span class='label label-success'>Devuelto</span>";
          }
        }},
        {data:"creada_por"},
        {data:"no_dispositivos"},
        {data: "", render: function(data, type, full, meta){
          if(full.estado == 'Asignado'){
            return "<a id='asignacion-devolver' data-id="+full.id+" class='btn btn-primary btn-devolver'>Devolver</a>";
          }else{
            return "";
          }
        }},
      ]
    });

    /** Devolver Asignación **/
    tabla.on('click', '.btn-devolver', function() {
      let data_fila = $(this).data();
      $.ajax({
        type: "POST",
        url: url_devolver,
        dataType: 'json',
        data: {
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          id: data_fila.id
        },
        success: function (response){
          bootbox.alert({message: "<h3><i class='fa fa-smile-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;REGISTRO ACTUALIZADO EXITOSAMENTE!!</h3></br>", className:"modal modal-success fade"});
          tabla.clear().draw();
          tabla.ajax.reload();
        },
        error: function (response){
          var mensaje = JSON.parse(response.responseText)
          bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.mensaje, className:"modal modal-danger fade"});
        }
      });
    });
  }
}

class InventarioInternoUpdate {
  constructor() {
    var urlTipoDispositivo = $("#asignacion-dispositivos-table").data("dispositivo");
    var urltable = $("#asignacion-dispositivos-table").data("url");
    var urlAprobar = $("#asignacion-dispositivos-table").data("apiaprobar");
    var urlRechazar = $("#asignacion-dispositivos-table").data("apirechazar");
    var urlReasignar = $("#id-reasignar").data("url");
    var urlUsuarios = $("#id-reasignar").data("urlusuarios");
    var urlEntregar = $("#id-entregar").data("url");
    var urlRedireccion = $("#id-entregar").data("urlredireccion");
    var pk = $("#asignacion-dispositivos-table").data("pk");

    /** CARGA DE DISPOSITIVOS ASIGNADOS A INVENTARIO INTERNO **/
    var tabla = $('#asignacion-dispositivos-table').DataTable({
      searching: true,
      paging:true,
      ordering: true,
      processing: true,
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      "order": [[4, "desc"]],
      ajax: {
        url: urltable,
        dataSrc: '',
        cache: true,
        data: {
          no_asignacion: pk
        }
      },
      columns: [
        {data: "asignacion_dispositivo"},
        {data: "",render: function(data, type, full, meta){
          return full.dispositivo.tipo;
        }},
        {data:"fecha_creacion", render: function(data, type, full, meta){
         var newDate = new Date(full.fecha_creacion);
         var options = {year: 'numeric', month:'long', day:'numeric', hour:'numeric',minute:'numeric'};
          return newDate.toLocaleDateString("es-Es",options);
        }},
        {data: "asignado_por"},
        {data: "",render: function(data, type, full, meta){
          return full.dispositivo.triage;
        }},
        {data: "",render: function(data, type, full, meta){
          if(full.fecha_aprobacion == null){
            return "<a id='dispositivo-aprobar' data-id="+full.id+"  class='btn btn-success btn-aprobar-dispositivo'>Aprobar</a>";
            
          }else{
            return "<span class='label label-success'>Aprobado</span>"
          }
        }},
        {data: "",render: function(data, type, full, meta){
          if(full.fecha_aprobacion == null){
            return "<a id='dispositivo-rechazar' data-id="+full.id+"  class='btn btn-warning btn-rechazar-dispositivo'>Rechazar</a>";
          }else{
            return "";
          }

        }},
      ]
    });

    /** Aprobar detalle de asignación **/
    tabla.on('click', '.btn-aprobar-dispositivo', function() {
      let data_fila = $(this).data();
      $.ajax({
        type: "POST",
        url: urlAprobar,
        dataType: 'json',
        data: {
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          detalle: data_fila.id
        },
        success: function (response){
          tabla.clear().draw();
          tabla.ajax.reload();
        },
        error: function (response){
          var mensaje = JSON.parse(response.responseText)
          bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
        }
      });
    });

    /** Rechazar detalle de asignación **/
    tabla.on('click', '.btn-rechazar-dispositivo', function() {
      let data_fila = $(this).data();
      bootbox.confirm({
        message: "¿Está seguro que quiere rechazar este dispositivo?",
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
            bootbox.prompt({
              title: "Ingrese el motivo de rechazo:",
              inputType: 'textarea',
              callback: function (result) {
                $.ajax({
                  type: "POST",
                  url: urlRechazar,
                  dataType: 'json',
                  data: {
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                    detalle: data_fila.id,
                    comentario: result
                  },
                  success: function (response){
                    tabla.clear().draw();
                    tabla.ajax.reload();
                  },
                  error: function (response){
                    var mensaje = JSON.parse(response.responseText)
                    bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje['mensaje'], className:"modal modal-danger fade"});
                  }
                });
              }
            });
          }
        }
      });
    });

    /** Cargar dispositivos solicitados para asignación de inventario interno al seleccionar tipo de dispositivo **/
    $('#id_tipo_dispositivo').change(function() {
      if($(this).val() != ""){
        var tipo = $(this).val();
        var no_asignacion = $('input[name="hdn_asignacion_id"]').val()
        var data_result = []
        $.ajax({
          url: urlTipoDispositivo,
          dataType:'json',
          data:{
            tipo: tipo,
            inventario_interno: no_asignacion,
          },
          error:function(){
            console.log("Error");
          },
          success:function(data){
            $("#id_dispositivo").empty();
            for (var i in data){
              data_result.push('<option value='+data[i].id+ '>'+data[i].triage+'</option>');
            }
            $("#id_dispositivo").append(data_result);
          }
        });
      }
    });

    /** Submit Form - Asignación de Dispositivos a Inventario Interno**/
    $('#frm_detalleform').submit(function(e) {
      e.preventDefault()
      $.ajax({
        type:"POST",
        url: $('#frm_detalleform').attr('action'),
        data: $('#frm_detalleform').serialize(),
        success: function(response) {
          console.log("Datos ingresados correctamente");
        },
        error: function(response) {
          var mensaje = JSON.parse(response.responseText)
          bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.error[0], className:"modal modal-danger fade"});
        }
      });
        //Limpiar fields de form detalle
        $('#id_tipo_dispositivo').select2("destroy").select2();
        $('#id_tipo_dispositivo').select2("val", "");
        $('#id_dispositivo').select2("destroy").select2();
        $('#id_dispositivo').select2("val", "");
        $('#id_dispositivo').html('');
        tabla.clear().draw();
        tabla.ajax.reload();
        location.reload();
    });
    //Inicio de boton reasignar usuario
    $('#id-reasignar').click( function() {
      $.ajax({
        url: urlUsuarios,
        data: function() {
          return {
            asignacion: pk
          }
        },
        error: function(response) {
          var mensaje = JSON.parse(response.responseText)
          bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.error[0], className:"modal modal-danger fade"});
        },
        success: function(data) {
          var listaUsuarios = [];
          for (var i in data){
            var usuario = {}
            usuario['text'] = data[i].full_name;
            usuario['value'] = data[i].id;
            listaUsuarios.push(usuario)
          }
          bootbox.prompt({
            title: "Seleccione el Usuario",
            inputType: 'select',
            inputOptions: listaUsuarios,
            callback: function (result) {
              $.ajax({
                type: "POST",
                url: urlReasignar,
                data: {
                  csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                  data:result,
                  id_asignacion: pk
                },
                success: function (response){
                  bootbox.alert({message: "<h3><i class='fa fa-smile-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;REGISTRO ACTUALIZADO EXITOSAMENTE!!</h3></br>", className:"modal modal-success fade"});
                  location.reload();
                },
                error: function (response){
                  var mensaje = JSON.parse(response.responseText)
                  bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.detail, className:"modal modal-danger fade"});
                }
              });
            }
          });
        }
      });
    });

    $('#id-entregar').click(function () {
      bootbox.confirm({
        message: "¿Está seguro que deseas entregar el equipo?",
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
          if (result == true){
            $.ajax({
              type: "POST",
              url: urlEntregar,
              dataType: 'json',
              data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                id: pk
              },
              success: function (response){
                bootbox.alert({message: "<h3><i class='fa fa-smile-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;REGISTRO ACTUALIZADO EXITOSAMENTE!!</h3></br>", className:"modal modal-success fade"});
                window.location = urlRedireccion
              },
              error: function (response){
                var mensaje = JSON.parse(response.responseText)
                bootbox.alert({message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.mensaje, className:"modal modal-danger fade"});
              }
            });
          }
        }
      });
    });
  }
}

class InventarioInternoList {
  constructor() {
    var url_api = $("#asignacion-list-form").attr("action");
    var tabla = $('#asignacion-table').DataTable({
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      processing: true,
      ajax: {
        url: url_api,
        deferRender: true,
        dataSrc: '',
        cache: true,
        data: function() {
          return $('#asignacion-list-form').serializeObject(true);
        }
      },
      columns: [
        {data: "no_asignacion.no_asignacion", render: function(data, type, full, meta){
          return "<a target='_blank' rel='noopener noreferrer' href="+full.no_asignacion.detail_url+" class='btn btn-success'>"+data+"</a>";
        }},
        {data: "dispositivo.triage", render: function(data, type, full, meta){
          return "<a target='_blank' rel='noopener noreferrer' href="+full.dispositivo.url+">"+data+"</a>";
        }},
        {data:"dispositivo.tipo"},
        {data:"no_asignacion.colaborador_asignado"},
        {data:"no_asignacion.fecha_asignacion"},
        {data:"no_asignacion.fecha_devolucion", render: function(data, type, full, meta){
          if(full.no_asignacion.fecha_devolucion){
            var newDate = new Date(full.no_asignacion.fecha_devolucion);
            return newDate.getFullYear()+'-' + (newDate.getMonth()+1) + '-'+newDate.getDate();
          } else {
            return "";
          }
         
        }},
        {data: "no_asignacion.estado", render: function(data, type, full, meta){
          if(full.no_asignacion.estado == 'Borrador'){
            return "<span class='label label-danger'>Borrador</span>";
          }else if(full.no_asignacion.estado == 'Asignado'){
            return "<span class='label label-warning'>Asignado</span>";
          } else {
            return "<span class='label label-success'>Devuelto</span>";
          }
        }},
      ]
    }).on('xhr.dt', function(e, settings, json, xhr) {
      $('#spinner').hide();
    });

    $('#asignacion-list-form').submit(function(e) {
      e.preventDefault();
      $('#spinner').show();
      tabla.clear().draw();
      new BuscadorTabla();
      tabla.ajax.reload();
    });
  }
}

class BuscadorTabla{
  constructor(){
    $('.dataTable tfoot th').each( function () {
      var title = $(this).text();
      $(this).html( '<input style="width:100%;box-sizing:border-box;" type="text" class="form-control input-sm" placeholder="Search '+title+'" />' );
  } );
  $('.dataTable').DataTable().columns().every( function (){
    var that = this;
    $('input',this.footer()).on('keyup change clear', function(){
      if(that.search()!==this.value){
        that.search(this.value).draw();
      }
    });
  });
  }
}




class InventarioInternoDetail {
  constructor() {
    var urlReasignar = $("#id-reasignar").data("url");
    var urlUsuarios = $("#id-reasignar").data("urlusuarios");
    var pk = $("#id-reasignar").data("pk");

    $('#id-reasignar').click(function() {
      $.ajax({
        url: urlUsuarios,
        data: function() {
          return {
            asignacion: pk
          }
        },
        error: function(response) {
          var mensaje = JSON.parse(response.responseText)
          bootbox.alert({
            message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.error[0],
            className: "modal modal-danger fade"
          });
        },
        success: function(data) {
          var listaUsuarios = [];
          for (var i in data) {
            var usuario = {}
            usuario['text'] = data[i].full_name;
            usuario['value'] = data[i].id;
            listaUsuarios.push(usuario)
          }
          bootbox.prompt({
            title: "Seleccione el Usuario",
            inputType: 'select',
            inputOptions: listaUsuarios,
            callback: function(result) {
              if (result) {
                bootbox.confirm({
                  message: "<h3><i class='fa fa-question-circle' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;¿Está seguro de efectuar el cambio de persona?</h3>",
                  className: "modal modal-warning fade",
                  callback: function(confirmacion) {
                    if (confirmacion) {
                      $.ajax({
                        type: "POST",
                        url: urlReasignar,
                        data: {
                          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                          data: result,
                          id_asignacion: pk
                        },
                        success: function(response) {
                          bootbox.alert({
                            message: "<h3><i class='fa fa-smile-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;REGISTRO ACTUALIZADO EXITOSAMENTE!!</h3></br>",
                            className: "modal modal-success fade"
                          });
                          location.reload();
                        },
                        error: function(response) {
                          var mensaje = JSON.parse(response.responseText)
                          bootbox.alert({
                            message: "<h3><i class='fa fa-frown-o' style='font-size: 45px;'></i>&nbsp;&nbsp;&nbsp;HA OCURRIDO UN ERROR!!</h3></br>" + mensaje.detail,
                            className: "modal modal-danger fade"
                          });
                        }
                      });
                    }
                  }
                });
              }
            }
          });
        }
      });
    });
  }
}