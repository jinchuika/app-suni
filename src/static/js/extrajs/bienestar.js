/***************************** FUNCIONES GENERALES ****************************************/
// Listar personas en riesgo de acuerdo a filtros seleccionados.
function listar_riesgo(span_input) {
  $(span_input).html('0');
  $.get($(span_input).data('url'),
  {
    colaborador: $('#bienestar-list-form #id_colaborador').val(),
    fecha_inicial: $('#bienestar-list-form #id_fecha_min').val(),
    fecha_fin: $('#bienestar-list-form #id_fecha_max').val()
  },
  function (respuesta) {
    $(span_input).html(respuesta.cantidad)
  });
}



/******************* BIENESTAR INFORME *********************************************/
(function (BienestarInforme, $, undefined) {
  let bienestar_form = $('#bienestar-list-form');

  // Cargar Histórico de resultados
  var tablaPrecio = $('#bienestar-table-search').DataTable({
    dom: 'Bfrtip',
    buttons: ['excel', 'pdf', 'copy'],
    processing:true,
    autoWidth:false,
    ajax:{
      type:"POST",
      url: bienestar_form.attr('action'),
      deferRender:true,
      dataSrc:'',
      cache:true,
      data:function () {
        return bienestar_form.serialize(true);
      },
    },
    columns: [
    {data: "fecha"},
    {data: "correo"},
    {data: "nombre"},
    {data: "edad"},
    {data: "dpi"},
    {data: "pregunta1"},
    {data: "pregunta2"},
    {data: "pregunta3"},
    {data: "pregunta4"},
    {data: "pregunta5"},
    {data: "pregunta6"},
    {data: "pregunta7"},
    {data: "pregunta8"},
    {data: "pregunta9"},
    {data: "pregunta10"},
    {data: "pregunta11"},
    {data: "pregunta12"},
    {data: "pregunta13"},
    {data: "pregunta14"},
    {data: "pregunta15"},
    {data: "pregunta16"},
    {data: "pregunta17"}
    ],
    columnDefs: [
    { "width": "150px", "targets":0 }
    ]
  }).on('xhr.dt', function(e, settings, json, xhr) {
    $('#spinner').hide();
  });

  /*Inicialización de clase BienestarInforme*/
  BienestarInforme.init = function () {
    $('#spinner').hide();
    bienestar_form.submit(function (e) {
      e.preventDefault();
      $('#spinner').show();
      tablaPrecio.clear().draw();
      new BuscadorTabla();
      tablaPrecio.ajax.reload();
    });
  }
}(window.BienestarInforme = window.BienestarInforme || {}, jQuery));

class BienestarInforme2 {
  constructor() {
    let bienestar_form = $('#bienestar-list-form');
    // Cargar Histórico de resultados en table designado
    var tablaPrecio = $('#bienestar-table-search').DataTable({
      dom: 'Bfrtip',
      buttons: ['excel', 'pdf', 'copy'],
      searching:true,
      paging:true,
      ordering:true,
      processing:true,
      destroy:true,
      autoWidth:false,
      ajax:{
        type: 'GET',
        url: $('#bienestar-table-search').data("todo"),
        dataSrc:'',
        cache:false,
        processing:true,
        data:function (params)
        {
         return {
           inicio: 1,
           csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
         };
       }
     },
     columns: [
     {data: "fecha"},
     {data: "correo"},
     {data: "nombre"},
     {data: "edad"},
     {data: "dpi"},
     {data: "pregunta1"},
     {data: "pregunta2"},
     {data: "pregunta3"},
     {data: "pregunta4"},
     {data: "pregunta5"},
     {data: "pregunta6"},
     {data: "pregunta7"},
     {data: "pregunta8"},
     {data: "pregunta9"},
     {data: "pregunta10"},
     {data: "pregunta11"},
     {data: "pregunta12"},
     {data: "pregunta13"},
     {data: "pregunta14"},
     {data: "pregunta15"},
     {data: "pregunta16"},
     {data: "pregunta17"}
     ],
     columnDefs: [
     { "width": "150px", "targets":0 }
     ]
   });

    tablaPrecio.columns.adjust().draw();
    var ctx17 = document.getElementById('grafico-linea-tiempo-todos').getContext('2d');
    var ctx18 = document.getElementById('grafico-linea-tiempo-individual').getContext('2d');

    bienestar_form.submit(function (e){
      e.preventDefault();
      /**/
      /*linea tiempo seleccionar*/
      $.ajax({
       url:bienestar_form.attr('action'),
       dataType:'json',
       data:bienestar_form.serialize(),
       error:function(){
         console.log("Error");
       },
       success:function(data){
         var fecha_individual=[];
         var respuesta_no_individual=[];
         var respuesta_si_individual=[];
         for(var l=0;l<data.length;l++){
           fecha_individual.push(data[l].fecha);
           respuesta_si_individual.push(data[l].respuesta_si);
           respuesta_no_individual.push(data[l].respuesta_no);
         }
         /**/
         var myChart18 = new Chart(ctx18, {
           type: 'line',
           data: {
            labels:fecha_individual,
            datasets: [{
              label: 'Si',
              backgroundColor: 'rgb(255, 99, 132)',
              borderColor: 'rgb(255, 99, 132)',
              data: respuesta_si_individual,
              fill: false,
            }, {
              label: 'No',
              fill: false,
              backgroundColor: 'rgb(54, 162, 235)',
              borderColor: 'rgb(54, 162, 235)',
              data: respuesta_no_individual,
            }]
          },
          options: {
            responsive: true,
            title: {
              display: true,
              text: '¿ Has presentado fiebre, tos, dolor de garganta, síntomas gastrointestinales (diarrea y/o vómito)  o dificultad para respirar en la últimas 24 horas?'
            },
            tooltips: {
              mode: 'index',
              intersect: false,
            },
            hover: {
              mode: 'nearest',
              intersect: true
            },
            scales: {
              xAxes: [{
                display: true,
                scaleLabel: {
                  display: true,
                  labelString: 'Fechas'
                }
              }],
              yAxes: [{
                display: true,
                scaleLabel: {
                  display: true,
                  labelString: 'Valores'
                }
              }]
            }
          }
        });
       },
       type: 'POST'
     });
      /*fin ajax*/
      /**/
      /**/
       //console.log( bienestar_form.serialize(true));
       var tablaPrecio = $('#bienestar-table-search').DataTable({
         searching:true,
         paging:true,
         ordering:true,
         processing:true,
         destroy:true,
         autoWidth:false,
         ajax:{
           type: 'POST',
           url:bienestar_form.attr('action'),
           dataSrc:'',
           cache:false,
           processing:true,
           data: function () {
             return bienestar_form.serialize(true);
           }
         },
         columnDefs: [
         { width: 200, targets: 0 }
         ],
         columns: [
         {data: "fecha"},
         {data: "correo"},
         {data: "nombre"},
         {data: "edad"},
         {data: "dpi"},
         {data: "pregunta1"},
         {data: "pregunta2"},
         {data: "pregunta3"},
         {data: "pregunta4"},
         {data: "pregunta5"},
         {data: "pregunta6"},
         {data: "pregunta7"},
         {data: "pregunta8"},
         {data: "pregunta9"},
         {data: "pregunta10"},
         {data: "pregunta11"},
         {data: "pregunta12"},
         {data: "pregunta13"},
         {data: "pregunta14"},
         {data: "pregunta15"},
         {data: "pregunta16"},
         {data: "pregunta17"}
         ],
       });
       /*Linea de tiempo*/

       /**/
     });
    /*chars*/
    var ctx1 = document.getElementById('grafico-pie-bienestar1').getContext('2d');
    var ctx3 = document.getElementById('grafico-pie-bienestar3').getContext('2d');
    var ctx4 = document.getElementById('grafico-pie-bienestar4').getContext('2d');
    var ctx5 = document.getElementById('grafico-pie-bienestar5').getContext('2d');
    var ctx7 = document.getElementById('grafico-pie-bienestar7').getContext('2d');
    var ctx9 = document.getElementById('grafico-pie-bienestar9').getContext('2d');
    var ctx10 = document.getElementById('grafico-pie-bienestar10').getContext('2d');
    var ctx12 = document.getElementById('grafico-pie-bienestar12').getContext('2d');
    var ctx14 = document.getElementById('grafico-pie-bienestar14').getContext('2d');
    var ctx15 = document.getElementById('grafico-pie-bienestar15').getContext('2d');
    var ctx16 = document.getElementById('grafico-pie-bienestar16').getContext('2d');

  //var ctxL = document.getElementById('timeline').getContext('2d');

  $.get($("#grafico-pie-bienestar1").data('url'),
   function (respuesta) {
     $.each(respuesta, function (index,datos) {
       var myChart1 = new Chart(ctx1, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{

             data: [datos.contador_si_pregunta1, datos.contador_no_pregunta1],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Padeces de alguna enfermedad o condición que te coloque en riesgo?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart1.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta1");
          }
        }
      });
       /**/
       var myChart3 = new Chart(ctx3, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{
             data: [datos.contador_si_pregunta3, datos.contador_no_pregunta3],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Tienes familiares que vivan contigo en esta época?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart3.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta3");

          }
        }
      });
       /**/
       var myChart4 = new Chart(ctx4, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{
             data: [datos.contador_si_pregunta4, datos.contador_no_pregunta4],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿ Has presentado fiebre, tos, dolor de garganta, síntomas gastrointestinales (diarrea y/o vómito)  o dificultad para respirar en la últimas 24 horas?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart4.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta4");
            alert(this.data.datasets[0].data[selectedIndex]);
          }
        }
      });
       /**/
       var myChart5 = new Chart(ctx5, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{
             data: [datos.contador_si_pregunta5, datos.contador_no_pregunta5],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Ha cambiado tu situación de salud desde la última vez que respondiste este formulario (solo responder del segundo en adelante)? '
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart5.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta5");
            alert(this.data.datasets[0].data[selectedIndex]);
          }

        }
      });
       /**/
       var myChart7 = new Chart(ctx7, {
         type: 'pie',
         data: {
           labels: ['Excelente', 'Bueno','Regular','Malo'],
           datasets: [{
             data: [datos.contador_excelente_pregunta7, datos.contador_bueno_pregunta7,datos.contador_regular_pregunta7,datos.contador_malo_pregunta7],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Cómo calificas tu estado emocional en este momento?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart7.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
                //actualizarTabla(selectedIndex,"pregunta7");
                actualizarTablaTipleOmas(selectedIndex,"pregunta7")
                console.log(selectedIndex);
                //alert(this.data.datasets[0].data[selectedIndex]);
              }
            }
          });
       /**/
       var myChart9 = new Chart(ctx9, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{
             data: [datos.contador_si_pregunta9, datos.contador_no_pregunta9],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Has registrado un cambio en cuanto al número de personas que viven contigo?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart9.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta9");
          }
        }
      });
       /**/
       var myChart10 = new Chart(ctx10, {
         type: 'pie',
         data: {
           labels: ['Si', 'No'],
           datasets: [{
             data: [datos.contador_si_pregunta10, datos.contador_no_pregunta10],
             backgroundColor: [
             colorRamdon(),
             colorRamdon(),
             ],

           }]
         },
         options: {
           responsive: true,
           title: {
            display: true,
            text: '¿Tienes algún familiar o personas en casa que en las últimas 24 horas haya presentado alguno de los síntomas anteriores?'
          },
          'onClick' : function (evt, item) {
            var activePoints = myChart10.getElementsAtEvent(evt);
            var selectedIndex = activePoints[0]._index;
            actualizarTabla(selectedIndex,"pregunta10");
          }
        }
      });
       /**/
       var myChart12 = new Chart(ctx12, {
        type: 'pie',
        data: {
          labels: ['Si', 'No'],
          datasets: [{
            data: [datos.contador_si_pregunta12, datos.contador_no_pregunta12],
            backgroundColor: [
            colorRamdon(),
            colorRamdon(),
            ],

          }]
        },
        options: {
          responsive: true,
          title: {
           display: true,
           text: '¿Tuviste contacto con algún caso confirmado o sospechoso de COVID-19?'
         },
         'onClick' : function (evt, item) {
           var activePoints = myChart12.getElementsAtEvent(evt);
           var selectedIndex = activePoints[0]._index;
           actualizarTabla(selectedIndex,"pregunta12");
           alert(this.data.datasets[0].data[selectedIndex]);
         }
       }
     });
       /**/
       var myChart14 = new Chart(ctx14, {
        type: 'pie',
        data: {
          labels: ['Si', 'No'],
          datasets: [{
            data: [datos.contador_si_pregunta14, datos.contador_no_pregunta14],
            backgroundColor: [
            colorRamdon(),
            colorRamdon(),
            ],

          }]
        },
        options: {
          responsive: true,
          title: {
           display: true,
           text: '¿Tiene tu colonia, municipio o comunidad donde vives cordón sanitario?'
         },
         'onClick' : function (evt, item) {
           var activePoints = myChart14.getElementsAtEvent(evt);
           var selectedIndex = activePoints[0]._index;
           actualizarTabla(selectedIndex,"pregunta14");

         }
       }
     });
       /**/
       var myChart15 = new Chart(ctx15, {
        type: 'pie',
        data: {
          labels: ['Si', 'No'],
          datasets: [{
            data: [datos.contador_si_pregunta15, datos.contador_no_pregunta15],
            backgroundColor: [
            colorRamdon(),
            colorRamdon(),
            ],

          }]
        },
        options: {
          responsive: true,
          title: {
           display: true,
           text: '¿ Tienes familiares o personas que vivan contigo en una casa que tenga labores de alta exposición de contacto? (repartidores de alimentos, medicina, o recepcionista?'
         },
         'onClick' : function (evt, item) {
           //console.log ('legend onClick', evt);
           //console.log('legd item', item);
           var activePoints = myChart15.getElementsAtEvent(evt);
           var selectedIndex = activePoints[0]._index;
           //console.log(selectedIndex);
           actualizarTabla(selectedIndex,"pregunta15");
           alert(this.data.datasets[0].data[selectedIndex]);
         }
       }
     });
       /**/
       var myChart16 = new Chart(ctx16, {
        type: 'pie',
        data: {
          labels: ['Si', 'No'],
          datasets: [{
            data: [datos.contador_si_pregunta16, datos.contador_no_pregunta16],
            backgroundColor: [
            colorRamdon(),
            colorRamdon(),
            ],

          }]
        },
        options: {
          responsive: true,
          title: {
           display: true,
           text: '¿Estás laborando actualmente en las instalaciones de la fundación?'
         },
         'onClick' : function (evt, item) {
           var activePoints = myChart16.getElementsAtEvent(evt);
           var selectedIndex = activePoints[0]._index;
           actualizarTabla(selectedIndex,"pregunta16");

         }
       }
     });
     });
});
/**/
function actualizarTabla(respuesta,pregunta) {
 var  respuesta_enviar="";
 var  pregunta_enviar=pregunta;
 if(respuesta==0){
   console.log("Si");
   respuesta_enviar="Si";
 }else{
   console.log("No");
   respuesta_enviar="No";
 }
 var tablaPrecio = $('#bienestar-table-search').DataTable({
   searching:true,
   paging:true,
   ordering:true,
   processing:true,
   destroy:true,
   ajax:{
     type: 'GET',
     url: $('#bienestar-table-search').data('url'),
     dataSrc:'',
     cache:false,
     processing:true,
     data: {
       pregunta:pregunta_enviar,
       respuesta:respuesta_enviar
     }
   },
   columns: [
   {data: "fecha"},
   {data: "correo"},
   {data: "nombre"},
   {data: "edad"},
   {data: "dpi"},
   {data: "pregunta1"},
   {data: "pregunta2"},
   {data: "pregunta3"},
   {data: "pregunta4"},
   {data: "pregunta5"},
   {data: "pregunta6"},
   {data: "pregunta7"},
   {data: "pregunta8"},
   {data: "pregunta9"},
   {data: "pregunta10"},
   {data: "pregunta11"},
   {data: "pregunta12"},
   {data: "pregunta13"},
   {data: "pregunta14"},
   {data: "pregunta15"},
   {data: "pregunta16"},
   {data: "pregunta17"}
   ],
 });
}

/**/
/**/
function actualizarTablaTipleOmas(respuesta,pregunta) {
 var  respuesta_enviar="";
 var  pregunta_enviar=pregunta;
 switch (respuesta) {
  case 0:
  respuesta_enviar="Excelente";
  break;
  case 1:
  respuesta_enviar="Bueno";
  break;
  case 2:
  respuesta_enviar="Regular";
  break;
  case 3:
  respuesta_enviar="Malo";
  break;
  default:
  console.log("error");
  break;
}
var tablaPrecio = $('#bienestar-table-search').DataTable({
 searching:true,
 paging:true,
 ordering:true,
 processing:true,
 destroy:true,
 ajax:{
   type: 'GET',
   url: $('#bienestar-table-search').data('url'),
   dataSrc:'',
   cache:false,
   processing:true,
   data: {
     pregunta:pregunta_enviar,
     respuesta:respuesta_enviar
   }
 },
 columns: [
 {data: "fecha"},
 {data: "correo"},
 {data: "nombre"},
 {data: "edad"},
 {data: "dpi"},
 {data: "pregunta1"},
 {data: "pregunta2"},
 {data: "pregunta3"},
 {data: "pregunta4"},
 {data: "pregunta5"},
 {data: "pregunta6"},
 {data: "pregunta7"},
 {data: "pregunta8"},
 {data: "pregunta9"},
 {data: "pregunta10"},
 {data: "pregunta11"},
 {data: "pregunta12"},
 {data: "pregunta13"},
 {data: "pregunta14"},
 {data: "pregunta15"},
 {data: "pregunta16"},
 {data: "pregunta17"}
 ],
});

}

/**/
function colorRamdon() {
 var chartColors = {
   red: 'rgb(255, 99, 132)',
   orange: 'rgb(255, 159, 64)',
   yellow: 'rgb(255, 205, 86)',
   green: 'rgb(75, 192, 192)',
   blue: 'rgb(54, 162, 235)',
   purple: 'rgb(153, 102, 255)',
   grey: 'rgb(201, 203, 207)',
   lime:	'rgb(0,255,0)',
   cyan: 	'rgb(0,255,255)',
   magenta: 'gb(255,0,255)',
   silver:	'rgb(192,192,192)',
   gray:	'rgb(128,128,128)',
   maroon:	'rgb(128,0,0)',
   olive:	'rgb(128,128,0)',
   green:	'rgb(0,128,0)',
   purple:	'rgb(128,0,128)',
   teal:	'rgb(0,128,128)',
   navy:	'rgb(0,0,128)',
   indian_red:	'rgb(205,92,92)',
   light_coral: 'rgb(240,128,128)'
 }
 var colorArray  = Object.keys(chartColors);
 var randomNumber = Math.random();
 var colorIndex  = Math.floor(randomNumber * colorArray.length);
 var randomKey    = colorArray[colorIndex];
 var randomValue  = chartColors[randomKey];
 return randomValue;
}
/**/
var fechas=[];
var respuesta_si=[];
var respuesta_no=[];
$.ajax({
 url:$('#grafico-linea-tiempo-todos').data("url"),
 dataType:'json',
 error:function(){
   console.log("Error");
 },
 success:function(data){
       //console.log(data);

       for(var k=0;k<data.length;k++){
        fechas.push(data[k].fecha);
        respuesta_si.push(data[k].si);
        respuesta_no.push(data[k].no);
      };
      /**/
      /**/
      var myChart17 = new Chart(ctx17, {
        type: 'line',
        data: {
         labels:fechas,
         datasets: [{
          label: 'Si',
          backgroundColor: 'rgb(255, 99, 132)',
          borderColor: 'rgb(255, 99, 132)',
          data: respuesta_si,
          fill: false,
        }, {
          label: 'No',
          fill: false,
          backgroundColor: 'rgb(54, 162, 235)',
          borderColor: 'rgb(54, 162, 235)',
          data: respuesta_no,
        }]
      },
      options: {
       responsive: true,
       title: {
        display: true,
        text: '¿ Has presentado fiebre, tos, dolor de garganta, síntomas gastrointestinales (diarrea y/o vómito)  o dificultad para respirar en la últimas 24 horas?'
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
         display: true,
         scaleLabel: {
          display: true,
          labelString: 'Fechas'
        }
      }],
      yAxes: [{
       display: true,
       scaleLabel: {
        display: true,
        labelString: 'Valores'
      }
    }]
  }
}
});
    },
    type: 'GET'
  }
  );
/*fin ajax*/



}

}
class BienestarGenerarGraficas {
  constructor() {
    $('#generar-graficas').click(function(){
      $.ajax({
        url:$('#generar-graficas').data("url"),
        dataType:'json',
        error:function(){
          console.log("Error");
        },
        success:function(data){
          bootbox.alert(data, function(){
            location.href = '/bienestar/resultadobienestarinforme/';
          });

        },
        type: 'GET'
      }
      );
      /*fin ajax*/
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
