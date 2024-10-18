class FormularioEvaluacion{
  constructor(){
    document.body.classList.add('loaded');
    const mySwiper = new Swiper('.swiper', {
      flipEffect: {
        limitRotation: true,
        slideShadows: true,
      },
      pagination: {
        el: '.swiper-pagination',
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      on: {
        init: function () {
          // Oculta el botón de "Enviar" al inicio
          document.querySelector('.btnEnviar').style.display = 'none';
        },
        slideChange: function () {
          const progress = (this.realIndex + 1) / this.slides.length * 100;
          document.querySelector('.progress-bar').style.width = `${progress}%`;
          document.querySelector('.progress-bar').setAttribute('aria-valuenow', progress);
  
          // Muestra u oculta los botones según la slide actual
          const prevButton = document.querySelector('.prevButton');
          const nextButton = document.querySelector('.nextButton');
          const enviarButton = document.querySelector('.btnEnviar');
  
          if (this.isEnd) {
            // Si es la última slide, oculta el botón Siguiente y muestra el botón Enviar
            nextButton.style.display = 'none';
            enviarButton.style.display = 'inline-block';
          } else {
            // Si no es la última slide, muestra el botón Siguiente y oculta el botón Enviar
            nextButton.style.display = 'inline-block';
            enviarButton.style.display = 'none';
          }
        },
      },
      allowSlidePrev: true,
      allowSlideNext: true,
    });
  
    const prevButton = document.querySelector('.prevButton');
    const nextButton = document.querySelector('.nextButton');
  
    prevButton.addEventListener('click', function () {
      mySwiper.slidePrev();
    });
  
    nextButton.addEventListener('click', function () {
      mySwiper.slideNext();
    });

  }
}


class FormularioList{
  constructor(){
  const url_participante = $("#formulario_list").data('url');
    $.ajax({
        url: url_participante, 
        method: 'GET',
        success: function(data) {
            data.formularios.forEach(formulario => {
                let progressBar = $('#progress-bar-' + formulario.sede);
                let tooltip = $('#tooltip-' + formulario.sede);
                
                // Actualizar el progreso de la barra
                if (progressBar.length) {
                    progressBar.css('width', formulario.porcentaje_completado + '%');
                    progressBar.text(formulario.porcentaje_completado + '%');
                }
                
                // Crear la lista de participantes faltantes
                let participantesFaltantes = formulario.lista_participantes_faltantes.join(', ');
                
                // Actualizar el tooltip con los participantes faltantes
                if (tooltip.length) {
                    tooltip.attr('title', 'Faltantes: ' + participantesFaltantes);
                    
                    // Activar el tooltip
                    tooltip.tooltip();
                }
            });
        },
        error: function(error) {
            console.error('Error al obtener los datos', error);
        }
    });
  }
}


class FormularioDetalle{
  constructor(){
        const url = $('#estadistica_detalle').data('url');
        const form = $('#estadistica_detalle').data('id');
        
        $.ajax({
          url: url, 
          data: { id: form },
          type: 'GET',
          dataType: 'json',
          success: function(response) {
      
              const preguntasTexto = response.datos.pregunta_texto;
              if (preguntasTexto.length >= 1) {
                  preguntasTexto.forEach(function (preguntaTexto) {
                      const preguntaID = `pregunta_${preguntaTexto.pregunta}`;
                      const canvasContainer = document.getElementById(preguntaID);
      
                      if (canvasContainer) {
                          preguntaTexto.respuestas.forEach((respuesta) => {
                              const respuestaElement = document.createElement('h5');
                              respuestaElement.textContent = respuesta;
                              canvasContainer.parentNode.insertBefore(respuestaElement, canvasContainer.nextSibling);
                          });
                      } else {
                          console.error(`No se encontró el elemento con ID: ${preguntaID}`);
                      }
                  });
              }
      
              const preguntas = response.datos.preguntas;
      
              preguntas.forEach(function(pregunta){
                  const tipoRespuesta = pregunta.tipo_respuesta;
                  const chartId = `myChart_${pregunta.pregunta}`;
                  const labels = pregunta.respuestas.map(respuesta => respuesta.respuesta);
                  const data = pregunta.respuestas.map(respuesta => respuesta.conteo);
                  const canvasElement = document.getElementById(chartId);
      
                  // Calcula el total de respuestas para cada pregunta
                  const totalRespuestas = data.reduce((a, b) => a + b, 0);
      
                  // Añade el porcentaje redondeado a las etiquetas
                  const labelsConPorcentaje = labels.map((label, index) => {
                      const porcentaje = Math.floor((data[index] / totalRespuestas) * 100); // Redondear sin decimales
                      return `${label} (${porcentaje}%)`;  // Etiqueta con porcentaje
                  });
      
                  if (canvasElement) {
                      if(tipoRespuesta == "Calidad"){
                          new Chart(canvasElement, {
                              type: 'doughnut',
                              data: {
                                  labels: labelsConPorcentaje,  // Usa las etiquetas con porcentaje redondeado
                                  datasets: [{
                                      label: labelsConPorcentaje,  // Etiquetas también aquí
                                      data: data,
                                      backgroundColor: [
                                          'rgba(0, 80, 255, 0.5)',
                                          'rgba(0, 180, 255, 0.5)',
                                          'rgba(0, 255, 255, 0.3)',
                                      ],
                                      borderColor: [
                                          'rgba(0, 80, 255, 1)',
                                          'rgba(0, 180, 255, 1)',
                                          'rgba(0, 255, 255, 1)',
                                      ],
                                      borderWidth: 1
                                  }],
                              },
                              options: {
                                  legend: { display: true },
                                  title: {
                                      display: false,
                                      text: 'Aja?'
                                  },
                              }
                          });
                      } else if(tipoRespuesta == "Booleana"){
                          new Chart(canvasElement, {
                              type: 'bar',
                              data: {
                                  labels: labelsConPorcentaje,  // Usa las etiquetas con porcentaje redondeado
                                  datasets: [{
                                      data: data,
                                      backgroundColor: [
                                          'rgba(129, 255, 125, 0.5)',
                                          'rgba(0, 221, 228, 0.4)',
                                      ],
                                      borderColor: [
                                          'rgba(81, 255, 75, 1)',
                                          'rgba(0, 221, 228, 1)',
                                      ],
                                      borderWidth: 2
                                  }]
                              },
                              options: {
                                  legend: { display: false },
                                  title: {
                                      display: false,
                                      text: ''
                                  },
                                  scales: {
                                      yAxes: [{
                                          ticks: {
                                              beginAtZero: true
                                          }
                                      }]
                                  }
                              }
                          });
                      } else if(tipoRespuesta == "Opinion"){
                          new Chart(canvasElement, {
                              type: 'doughnut',
                              data: {
                                  labels: labelsConPorcentaje,  // Usa las etiquetas con porcentaje redondeado
                                  datasets: [{
                                      label: labelsConPorcentaje,  // Etiquetas también aquí
                                      data: data,
                                      backgroundColor: [
                                          'rgba(255, 0, 255, 0.5)',
                                          'rgba(255, 150, 255, 0.5)',
                                      ],
                                      borderColor: [
                                          'rgba(255, 0, 255, 1)',
                                          'rgba(255, 150, 255, 1)',
                                      ],
                                      borderWidth: 1
                                  }]
                              }
                          });
                      }
                  }
              });
          },
          error: function(xhr, status) {
              alert('Error al cargar estadística');
          }
      });
      

  }
}


class InformeEvaluacion {
  constructor() {
    $('#evaluacion-informe').on('submit', this.envioForm);
  }

  envioForm(event) {
    event.preventDefault();
    const url = $('#evaluacion-informe').data('url');
    const formData = $('#evaluacion-informe').serialize();

    $.ajax({
      url: url,
      data: formData,
      type: 'GET',
      dataType: 'json',
      success: function (response) {
        const secciones = response.datos.secciones;
        const preguntas = response.datos.preguntas;
        const preguntasTexto = response.datos.pregunta_texto;
        const divContenedor = document.getElementById('estadistica_informe');

        divContenedor.innerHTML = ''; // Limpiar contenido previo

        secciones.forEach(function (seccion) {
          const seccionDiv = document.createElement('div');
          seccionDiv.className = 'text-center';

          const seccionTitulo = document.createElement('h1');
          seccionTitulo.textContent = `Sección: ${seccion}`;
          seccionDiv.appendChild(seccionTitulo);

          const boxDiv = document.createElement('div');
          boxDiv.className = 'box box-primary';

          const rowDiv = document.createElement('div');
          rowDiv.className = 'row';

          preguntas.forEach(function (pregunta) {
            if (pregunta.seccion_pregunta === seccion) {
              const preguntaDiv = document.createElement('div');
              preguntaDiv.className = 'col-8 col-md-3';

              const preguntaTitulo = document.createElement('h5');
              preguntaTitulo.textContent = pregunta.pregunta;
              preguntaDiv.appendChild(preguntaTitulo);

              if (pregunta.tipo_respuesta === 'Texto') {
                return; // No hacemos nada si es de tipo "Texto"
              } else {
                const canvas = document.createElement('canvas');
                canvas.id = `myChart_${pregunta.pregunta}`;
                canvas.width = 335;
                canvas.height = 360;
                preguntaDiv.appendChild(canvas);
              }

              rowDiv.appendChild(preguntaDiv);
            }
          });

          preguntasTexto.forEach(function (preguntaTexto) {
            if (preguntaTexto.seccion_pregunta === seccion) {
              const textoDiv = document.createElement('div');
              textoDiv.className = 'texto col-8 col-md-6';
              textoDiv.id = `pregunta_${preguntaTexto.pregunta}`;

              const preguntaTitulo = document.createElement('h4');
              preguntaTitulo.textContent = preguntaTexto.pregunta;
              textoDiv.appendChild(preguntaTitulo);

              preguntaTexto.respuestas.forEach(function (respuesta) {
                const respuestaParrafo = document.createElement('p');
                respuestaParrafo.textContent = respuesta;
                textoDiv.appendChild(respuestaParrafo);
              });

              rowDiv.appendChild(textoDiv);
            }
          });

          boxDiv.appendChild(rowDiv);
          seccionDiv.appendChild(boxDiv);
          divContenedor.appendChild(seccionDiv);
        });

        preguntas.forEach(function (pregunta) {
          const tipoRespuesta = pregunta.tipo_respuesta;
          const chartId = `myChart_${pregunta.pregunta}`;
          const labels = pregunta.respuestas.map((respuesta) => respuesta.respuesta);
          const data = pregunta.respuestas.map((respuesta) => respuesta.conteo);
          const canvasElement = document.getElementById(chartId);

          // Calcular el total de respuestas para cada pregunta
          const totalRespuestas = data.reduce((a, b) => a + b, 0);

          // Calcular porcentajes sin redondear
          let porcentajes = data.map((conteo) => (conteo / totalRespuestas) * 100);

          // Redondear los porcentajes y ajustar la suma a 100%
          let porcentajesRedondeados = porcentajes.map(Math.floor);
          let sumaRedondeados = porcentajesRedondeados.reduce((a, b) => a + b, 0);

          // Si la suma no es 100, ajustar el valor más cercano
          let diferencia = 100 - sumaRedondeados;
          if (diferencia !== 0) {
            let indexAjuste = porcentajes.indexOf(Math.max(...porcentajes));
            porcentajesRedondeados[indexAjuste] += diferencia; // Ajustar el más grande
          }

          // Crear etiquetas con porcentaje ajustado
          const labelsConPorcentaje = labels.map((label, index) => {
            return `${label} (${porcentajesRedondeados[index]}%)`;  // Etiqueta con porcentaje redondeado ajustado
          });

          if (canvasElement) {
            if (tipoRespuesta === "Calidad") {
              new Chart(canvasElement, {
                type: 'doughnut',
                data: {
                  labels: labelsConPorcentaje, // Usar etiquetas con porcentaje ajustado
                  datasets: [{
                    label: labelsConPorcentaje,
                    data: data,
                    backgroundColor: [
                      'rgba(0, 80, 255, 0.5)',
                      'rgba(0, 180, 255, 0.5)',
                      'rgba(0, 255, 255, 0.3)',
                    ],
                    borderColor: [
                      'rgba(0, 80, 255, 1)',
                      'rgba(0, 180, 255, 1)',
                      'rgba(0, 255, 255, 1)',
                    ],
                    borderWidth: 1,
                  }],
                },
                options: {
                  legend: { display: true },
                  title: {
                    display: false,
                  },
                },
              });
            } else if (tipoRespuesta === "Opinion") {
              new Chart(canvasElement, {
                type: 'doughnut',
                data: {
                  labels: labelsConPorcentaje, // Usar etiquetas con porcentaje ajustado
                  datasets: [{
                    label: labelsConPorcentaje,
                    data: data,
                    backgroundColor: [
                      'rgba(255, 0, 255, 0.5)',
                      'rgba(255, 150, 255, 0.5)',
                    ],
                    borderColor: [
                      'rgba(255, 0, 255, 1)',
                      'rgba(255, 150, 255, 1)',
                    ],
                    borderWidth: 1,
                  }],
                },
              });
            } else if (tipoRespuesta === 'Booleana') {
              new Chart(canvasElement, {
                type: 'bar',
                data: {
                  labels: labelsConPorcentaje, // Usar etiquetas con porcentaje ajustado
                  datasets: [{
                    data: data,
                    backgroundColor: ['rgba(129, 255, 125, 0.5)', 'rgba(0, 221, 228, 0.4)'],
                    borderColor: ['rgba(81, 255, 75, 1)', 'rgba(0, 221, 228, 1)'],
                    borderWidth: 2,
                  }],
                },
                options: {
                  legend: { display: false },
                  scales: {
                    yAxes: [{ ticks: { beginAtZero: true } }],
                  },
                },
              });
            }
          }
        });
      },
      error: function (xhr, status) {
        alert('Error al cargar estadística');
      },
    });
  }
}
