var new_marcas =[];
var marcas=[];
var encabezado = [];
var nuevo_marca=[];
var datos =[];
var new_data=[];
var actualizar = [];
var linea =[];
var result=[];
var puertos=[];
var new_velocidad=[];
var dispositivo;
var sistema =[];
var procesador=[];
var hdd=[];
var tipos_monitores =[];
var os =[];
var cargador=[];
var estuche= [];
var protector= [];

var urldispositivo = $("#grid_id").data("url");
$.ajax({
  type: 'POST',  
  url: $('#grid_id').data('dispo'), 
  dataType: 'json', 
  data: {
    paquete:$('#grid_id').data('id'),    
    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
   
  },
  success: function (response) {
    
    marcas = response.marcas;
    datos=response.data;

    dispositivo = response.dispositivo
    sistema = response.sistemas
    nueva_data =JSON.stringify(datos[0]).toString()    
    var separators = [':',',', '\\\{', '\\\}'];
    var tokens = nueva_data.split(new RegExp(separators.join('|'), 'g'));
    for(c=0;c<tokens.length; c++){
      if(c % 2){
        /*Aca es para obtener los encabezados que vamos a mostrar en el grid separando
         "tipo":"TECLADO" y solo obteniendo "tipo" y lo guardamos en una lista
        */
        var token_sin = tokens[c].replace(/['"]+/g,'');
        var name = token_sin.charAt(0).toUpperCase() + token_sin.slice(1);
        ////
        if (name =="Marca__marca"){
                  name ="Marca";
                }
                if (name =="Puerto__nombre"){
                  name ="Puerto";
                }
                if (name =="Cantidad_puertos"){
                  name ="Cantidad puertos";
                }
                if (name =="Velocidad_medida"){
                  name ="Velocidad medida";
                }
                if (name =="Tipo_mouse"){
                  name ="Tipo Mouse";
                }
                if (name =="Version_sistema"){
                  name ="Version Sistema";
                }
                if (name =="So_id"){
                  name ="Sistema Operativo";
                }
                if (name =="Medida_almacenamiento"){
                  name ="Medida";
                }
                if (name =="Medida_ram" || name=="Ram_medida"){
                  name ="Medida ram";
                }
                if (name =="Almacenamiento_externo"){
                  name ="Externo";
                }
                if (name =="Disco_duro__triage"){
                  name ="Disco duro";
                }
                if (name =="All_in_one"){
                  name ="All in one";
                }
                if (name =="Tipo_monitor"){
                  name ="Tipo monitor";
                }
                if (name =="Cargador__triage"){
                  name ="Cargador";
                }
                if (name =="Estuche__triage"){                      
                  name ="Estuche";
                }
                if (name =="Protector__triage"){                      
                  name ="Protector";
                }
                //Creacion de los encabezados y obtenecion de la linea que se modifico en el grid
                if(name=="Id" || name=="Url" || name=="Entrada" || name=="Estado" || name=="Etapa" || name=="Tarima"){
                }else{
                  //
                  if(name=="Triage"){
                    encabezado.push({title:name,name:token_sin,
                      onBeforeChange: function(ev){
                                console.log('Before change:' + ev);
                            },
                            onAfterChange: function(ev){
                              console.log('After change:' + ev);
                              linea.push(ev.rowKey);
                            },});
                  }else{
                    if(name !="Marca"){
                      if(name =="Puerto"){
                        encabezado.push({title:name,name:token_sin,
                          onBeforeChange: function(ev){
                                    console.log('Before change:' + ev);
                                },
                                onAfterChange: function(ev){
                                  console.log('After change:' + ev);
                                  linea.push(ev.rowKey);
                                }, editOptions: {
                                type: 'select',
                                listItems:puertos,
                                useViewMode: true
                            },
                            copyOptions:{
                              useListItemText:true
                            },
                            component :{
                              name:'select2'
                            }});

                      }else{
                        if(name == "Velocidad medida"){
                          encabezado.push({title:name,name:token_sin,
                            onBeforeChange: function(ev){
                                      console.log('Before change:' + ev);
                                  },
                                  onAfterChange: function(ev){
                                    console.log('After change:' + ev);
                                    linea.push(ev.rowKey);
                                  }, editOptions: {
                                  type: 'select',
                                  listItems:new_velocidad,
                                  useViewMode: true
                              },
                              copyOptions:{
                                useListItemText:true
                              },
                              component :{
                                name:'select2'
                              }});
                        }else{
                          if(name == "Version Sistema"){
                            encabezado.push({title:name,name:token_sin,
                              onBeforeChange: function(ev){
                                        console.log('Before change:' + ev);
                                    },
                                    onAfterChange: function(ev){
                                      console.log('After change:' + ev);
                                      linea.push(ev.rowKey);
                                    }, editOptions: {
                                    type: 'select',
                                    listItems:sistema,
                                    useViewMode: true
                                },
                                copyOptions:{
                                  useListItemText:true
                                },
                                component :{
                                  name:'select2'
                                }});

                          }else{
                            if(name=="Medida ram" || name=="Medida"){
                              encabezado.push({title:name,name:token_sin,
                                onBeforeChange: function(ev){
                                          console.log('Before change:' + ev);
                                      },
                                      onAfterChange: function(ev){
                                        console.log('After change:' + ev);
                                        linea.push(ev.rowKey);
                                      }, editOptions: {
                                      type: 'select',
                                      listItems:new_velocidad,
                                      useViewMode: true
                                  },
                                  copyOptions:{
                                    useListItemText:true
                                  },
                                  component :{
                                    name:'select2'
                                  }});
                            }else{
                              if(name=="Procesador"){
                                encabezado.push({title:name,name:token_sin,
                                  onBeforeChange: function(ev){
                                            console.log('Before change:' + ev);
                                        },
                                        onAfterChange: function(ev){
                                          console.log('After change:' + ev);
                                          linea.push(ev.rowKey);
                                        },
                                        editOptions: {
                                        type: 'select',
                                        listItems:procesador,
                                        useViewMode: true
                                    },
                                    copyOptions:{
                                      useListItemText:true
                                    },
                                    component :{
                                      name:'select2'
                                    }});

                              }else{
                                if(name=="Disco duro"){
                                  encabezado.push({title:name,name:token_sin,
                                    onBeforeChange: function(ev){
                                              console.log('Before change:' + ev);
                                          },
                                          onAfterChange: function(ev){
                                            console.log('After change:' + ev);
                                            linea.push(ev.rowKey);
                                          }, editOptions: {
                                          type: 'select',
                                          listItems:hdd,
                                          useViewMode: true
                                      },
                                      copyOptions:{
                                        useListItemText:true
                                      },
                                      component :{
                                        name:'select2'
                                      }});
                                }else{
                                  if(name=="Tipo monitor"){
                                    encabezado.push({title:name,name:token_sin,
                                      onBeforeChange: function(ev){
                                                console.log('Before change:' + ev);
                                            },
                                            onAfterChange: function(ev){
                                              console.log('After change:' + ev);
                                              linea.push(ev.rowKey);
                                            }, editOptions: {
                                            type: 'select',
                                            listItems:tipos_monitores,
                                            useViewMode: true
                                        },
                                        copyOptions:{
                                          useListItemText:true
                                        },
                                        component :{
                                          name:'select2'
                                        }});
                                  }else{
                                    if(name=="Sistema Operativo"){
                                      encabezado.push({title:name,name:token_sin,
                                        onBeforeChange: function(ev){
                                                  console.log('Before change:' + ev);
                                              },
                                              onAfterChange: function(ev){
                                                console.log('After change:' + ev);
                                                linea.push(ev.rowKey);
                                              }, editOptions: {
                                              type: 'select',
                                              listItems:os,
                                              useViewMode: true
                                          },
                                          copyOptions:{
                                            useListItemText:true
                                          },
                                          component :{
                                            name:'select2'
                                          }});
                                    }else{
                                      if(name=="Servidor" || name=="All in one" || name=="Externo"){
                                        encabezado.push({title:name,name:token_sin,
                                               onBeforeChange: function(ev){
                                                    console.log('Before change:' + ev);
                                                },
                                                onAfterChange: function(ev){
                                                  console.log('After change:' + ev);
                                                  linea.push(ev.rowKey);
                                                }, editOptions: {
                                              type: 'checkbox',
                                              listItems:[{text:"Si",value:'true'}],
                                              useViewMode: false
                                            }});
                                      }else{
                                        if(name=="Clase"){
                                          encabezado.push({title:name,name:token_sin,
                                                 onBeforeChange: function(ev){
                                                      console.log('Before change:' + ev);
                                                  },
                                                  onAfterChange: function(ev){
                                                    console.log('After change:' + ev);
                                                    linea.push(ev.rowKey);
                                                  }, editOptions: {
                                                type: 'select',
                                                listItems:[{text:"A",value:1},{text:"B",value:2},{text:"C",value:3}],
                                                useViewMode: true
                                              }});
                                        }else{
                                          if(name=="Cargador"){
                                            encabezado.push({title:name,name:token_sin,
                                              onBeforeChange: function(ev){
                                                        console.log('Before change:' + ev);
                                                    },
                                                    onAfterChange: function(ev){
                                                      console.log('After change:' + ev);
                                                      linea.push(ev.rowKey);
                                                    }, editOptions: {
                                                    type: 'select',
                                                    listItems:cargador,
                                                    useViewMode: true
                                                },
                                                copyOptions:{
                                                  useListItemText:true
                                                },
                                                component :{
                                                  name:'select2'
                                                }});
                                            }else{
                                                /* */
                                                if(name=="Estuche"){
                                                  encabezado.push({title:name,name:token_sin,
                                                    onBeforeChange: function(ev){
                                                              console.log('Before change:' + ev);
                                                          },
                                                          onAfterChange: function(ev){
                                                            console.log('After change:' + ev);
                                                            linea.push(ev.rowKey);
                                                          }, editOptions: {
                                                          type: 'select',
                                                          listItems:estuche,
                                                          useViewMode: true
                                                      },
                                                      copyOptions:{
                                                        useListItemText:true
                                                      },
                                                      component :{
                                                        name:'select2'
                                                      }});
                                                  }else{
                                                    if(name=="Protector"){
                                                      encabezado.push({title:name,name:token_sin,
                                                        onBeforeChange: function(ev){
                                                                  console.log('Before change:' + ev);
                                                              },
                                                              onAfterChange: function(ev){
                                                                console.log('After change:' + ev);
                                                                linea.push(ev.rowKey);
                                                              }, editOptions: {
                                                              type: 'select',
                                                              listItems:protector,
                                                              useViewMode: true
                                                          },
                                                          copyOptions:{
                                                            useListItemText:true
                                                          },
                                                          component :{
                                                            name:'select2'
                                                          }});
                                                      }else{
                                                    if(name!=""){
                                                      encabezado.push({title:name,name:token_sin,
                                                             onBeforeChange: function(ev){
                                                                  console.log('Before change:' + ev);
                                                              },
                                                              onAfterChange: function(ev){
                                                                console.log('After change:' + ev);
                                                                linea.push(ev.rowKey);
                                                              }, editOptions: {
                                                            type: 'text',
                                                            maxLength: 50,
                                                            useViewMode: false
                                                          }});
                                                           }
                                                  }

                                                /**/
                                              }                                  

                                            }                                  
                                           
                                               }
                                            }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                          }
                      }
                    }else{
                        encabezado.push({title:name,name:token_sin,
                               onBeforeChange: function(ev){
                                    console.log('Before change:' + ev);
                                },
                                onAfterChange: function(ev){
                                  console.log('After change:' + ev);
                                  linea.push(ev.rowKey);
                                }, editOptions: {
                                type: 'select',
                                listItems:new_marcas,
                                useViewMode:true
                            }
                           });
                          }
                        }
                    //
                }



        ////

      }

    }  //fin del for
    //majeno de errores al momento que no vengan campos de los dispositivos
                    try {
                      for( k=0; k< response.marcas.length;k++){
                          var id = response.marcas[k].id
                          var texto = response.marcas[k].marca
                          var nuevo_ingreso = {text:texto,value:id.toString()}
                          new_marcas.push(nuevo_ingreso);
                      }
                    } catch (e) {
                      console.log("No usa este campo");
                    }
                    //
                    try {
                      for( l=0; l< response.puertos.length;l++){
                          var id_puertos = response.puertos[l].id
                          var texto_puertos = response.puertos[l].nombre
                          var nuevo_ingreso_puertos = {text:texto_puertos,value:id_puertos.toString()}
                          puertos.push(nuevo_ingreso_puertos);
                      }
                    } catch (e) {
                     console.log("No usa este campo");
                    }
                    //
                      try {
                        for( j=0; j< response.medida.length;j++){
                            var id_medida = response.medida[j].id
                            var texto_medida = response.medida[j].nombre
                            var nuevo_ingreso_medida = {text:texto_medida,value:id_medida.toString()}
                            new_velocidad.push(nuevo_ingreso_medida);
                        }
                      } catch (e) {
                       console.log("No usa este campo");
                      }
                      //
                      try {
                        for( a=0; a< response.sistemas.length;a++){
                            var id_sistema = response.sistemas[a].id
                            var texto_sistema = response.sistemas[a].nombre
                            var nuevo_ingreso_sistema = {text:texto_sistema,value:id_sistema.toString()}
                            sistema.push(nuevo_ingreso_sistema);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      }
                      //
                      try {
                        for( b=0; b< response.procesador.length;b++){
                            var id_procesador = response.procesador[b].id
                            var texto_procesador = response.procesador[b].nombre
                            var nuevo_ingreso_procesador = {text:texto_procesador,value:id_procesador.toString()}
                            procesador.push(nuevo_ingreso_procesador);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      }
                      //
                      try {
                        for( g=0; g< response.hdd.length;g++){
                            var id_hdd = response.hdd[g].triage
                            var texto_hdd = response.hdd[g].triage
                            var nuevo_ingreso_hdd = {text:texto_hdd,value:id_hdd.toString()}
                            hdd.push(nuevo_ingreso_hdd);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      }
                      //
                      try {
                        for( d=0; d< response.tipo.length;d++){
                            var id_tipo = response.tipo[d].id
                            var texto_tipo = response.tipo[d].tipo
                            var nuevo_ingreso_tipo = {text:texto_tipo,value:id_tipo.toString()}
                            tipos_monitores.push(nuevo_ingreso_tipo);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      }
                      //
                      try {
                        for( e=0; e< response.os.length;e++){
                            var id_os = response.os[e].id
                            var texto_os = response.os[e].nombre
                            var nuevo_ingreso_os = {text:texto_os,value:id_os.toString()}
                            os.push(nuevo_ingreso_os);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      }
                      //cargador
                      try {
                        for( f=0; f< response.cargador.length;f++){
                            var id_cargador = response.cargador[f].triage
                            var texto_cargador = response.cargador[f].triage
                            var nuevo_ingreso_cargador = {text:texto_cargador,value:id_cargador.toString()}
                            cargador.push(nuevo_ingreso_cargador);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      } 

                       //estuche o case
                       try {
                        for( t=0; t< response.estuche.length;t++){
                            var id_estuche = response.estuche[t].triage
                            var texto_estuche = response.estuche[t].triage
                            var nuevo_ingreso_estuche = {text:texto_estuche,value:id_estuche.toString()}
                            estuche.push(nuevo_ingreso_estuche);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      } 
                       //protector
                       try {
                        for( t=0; t< response.protector.length;t++){
                            var id_protector = response.protector[t].triage
                            var texto_protector = response.protector[t].triage
                            var nuevo_ingreso_protector = {text:texto_protector,value:id_protector.toString()}
                            protector.push(nuevo_ingreso_protector);
                        }
                      } catch (e) {
                        console.log("No usa este campo");
                      } 
    //Inicido del grid y  nombre de los encabezados
        grid = new tui.Grid({
           el: $('#grid'),
           scrollX: false,
           scrollY: false,
           columns: encabezado
       });
     grid.setData(datos);
  },
  error: function (response) {
    console.log(response);
  }
});
/*Funcion para actualizar los dispositivos de primero ordena  y elimina el numero de fila repetida despues
      obtenermos las filas del grid que vamos a actualizar y las enviamos por un POST
    */
    function actualizar_post(){
    var sorted_arr = linea.slice().sort();
      var result=[];
      for (var i=0; i< sorted_arr.length; i++){
        if (sorted_arr[i] != sorted_arr[i + 1]) {
            result.push(sorted_arr[i]);
        }
      }
      for (var k=0; k<result.length; k++){
        actualizar.push(grid.getRow(result[k]));
      }
      // post para actualizar los dispositivos
     $.ajax({
        type: 'POST',
        url: urldispositivo,
        dataType: 'json',
        data: {
          datos_actualizar :JSON.stringify(actualizar),
          dispositivo:dispositivo,
        },
        headers:{"X-CSRFToken":$('input[name="csrfmiddlewaretoken"]').val()},
        success: function (response) {
          bootbox.alert("Dispositivos actualizados correctamente");
          actualizar=[];
        },
        error: function (response) {
          //var jsonResponse = JSON.parse(response.responseText);
          bootbox.alert({message:"Error al ingresar datos", className:"modal modal-danger fade"});
          actualizar=[];
        }
      });
      //
    };
