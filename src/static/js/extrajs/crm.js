(function( HistoricoOfertas, $, undefined ) {
    var crear_historial_ofertas = function (url, id_solicitud, comentario){
      var data = {
        "id_historico":id_solicitud,
        "comentario":comentario
      }
      console.log(id_solicitud);
      $.post(url, JSON.stringify(data)).then(function (response){
        var fecha = new Date(response.fecha);
        var td_data = $('<td></td>').text(fecha.getDate()+"/"+(fecha.getMonth()+1)+"/"+fecha.getFullYear()+","+response.usuario);
        var td = $('<td></td>').text(response.comentario);
        var tr = $('<tr></tr>').append(td).append(td_data);
      $('#body-historial-' + id_solicitud).append(tr);

      },function(response){
        alert("Error al crear datos");
      });
    }


    // Public
    HistoricoOfertas.init = function () {
      $('.ofertaHistorico-btn').click(function (){
        var id_solicitud = $(this).data('id');
        var url = $(this).data('url');
        bootbox.prompt({
          title: "Historial de Ofertas",
          inputType: 'textarea',
          callback: function (result) {
            if (result) {
              crear_historial_ofertas(url, id_solicitud, result);

            }
          }
        });
      });
    }
}( window.HistoricoOfertas = window.HistoricoOfertas || {}, jQuery ));

(function( OfertasList, $, undefined ) {
    var tabla = $('#ofertas-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#ofertas-list-form').attr('action'),
            deferRender: true,
            dataSrc: '',
            cache:true,
            data: function () {
                return $('#ofertas-list-form').serializeObject(true);
            }
        },
        columns: [
          {data:"id",
          render: function(data, type, full, meta){
            return '<a href="'+full.url+'">'+data +'</a>'
          }},
          {data:"fecha_inicio",className:"nowrap"},
          {data:"donante",
          className:"nowrap",
          render:function(data, type, full, meta){
            return '<a href="'+full.urlDonante+'">'+data+'</a>'
          }},
          {data:"recibido",className:"nowrap"},
          {data:"fecha_bodega",className:"nowrap"},
          {data:"tipo_oferta",className:"nowrap"},
          {data:"fecha_carta", className:"nowrap"},
          {data:"contable", className:"nowrap"}

        ]

    }).on('xhr.dt', function (e, settings, json, xhr) {
        $('#spinner').hide();
    });

    // Public
    OfertasList.init = function () {
        $('#spinner').hide();
        $('#ofertas-list-form').submit(function (e) {
            e.preventDefault();
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();
        });
    }
}( window.OfertasList = window.OfertasList || {}, jQuery ));

(function( InformeDonante, $, undefined ) {
    var flag=false;
    var tabla = $('#donante-table').DataTable({
        dom: 'lfrtipB',
        buttons: ['excel','pdf'],
        processing: true,
        ajax: {
            url: $('#donante-list-form').attr('action'),
            deferRender: true,
            dataSrc: 'data',
            cache:true,
            data: function () {
                return $('#donante-list-form').serializeObject(true);
            }
        },
        columns: [
          
          {data:"donante",className:"nowrap"},
          {data:"tipoDispositivo",className:"nowrap"},
          {data:"cantidad",className:"nowrap"},
          {
            data:"precioUnitario",
            className:"nowrap",
            render: function(data){
              return formatCurrency(data);
            }
          },
          {
            data:"total", 
            className:"nowrap",
            render: function(data){
              return formatCurrency(data);
            }
          },
        ]

    }).on('xhr.dt', function (e, settings, json, xhr) {
      $('#spinner').hide();
      if (json && json.totales) {
        $('#total-cantidad').text(json.totales.cantidad_total);
        $('#total-monto').text(formatCurrency(json.totales.monto_total));
      }
      if(!flag){
        return;
      }
      if (json && json.valores && json.dispositivos && json.montos) {
        if (window.general_chart) {
          window.general_chart.destroy();
        }
               
        window.general_chart = new Chart(document.getElementById("proveedor_chart_bar"), {
          type: 'bar',
          data: {
            labels: json.dispositivos,
            datasets: [{
              label:"Dispositivos del proveedor",
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              data: json.valores,
              topLabels: (function() {
                  let lista = [];
                  for (let i = 0; i < json.montos.length; i++) {
                      lista.push(formatCurrency(json.montos[i]));
                  }
                  return lista;
              })()
            }]
          },
          options: {
            title: {
              display: true,
              text: "Gráfica de Dispositivos"
            },
            scales: {
              x: {
                    ticks: {
                        autoSkip: true,  
                        maxRotation: 0,   
                        minRotation: 0     
                    }
                },
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              datalabels: {
                  color: '#000',
                  anchor: 'end',
                  align: 'top',
                  font: {
                      weight: 'bold'
                  },
                  
                  formatter: (value, context) => {
                      return context.dataset.topLabels[context.dataIndex];
                  }
                }
            }
          }      
        }
      );
      }
        
    });

    const formatCurrency = (valor) => {
    return new Intl.NumberFormat('es-GT', {
        style: 'currency',
        currency: 'GTQ'
    }).format(valor);
    };

    // Public
    InformeDonante.init = function () {
        $('#spinner').hide();
        $('#donante-list-form').submit(function (e) {
            e.preventDefault();
            flag=true;
            $('#spinner').show();
            tabla.clear().draw();
            tabla.ajax.reload();

        });
    }
}( window.InformeDonante = window.InformeDonante || {}, jQuery ));