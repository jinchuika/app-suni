// Archivo: swiper-scripts.js

document.addEventListener('DOMContentLoaded', function () {
  document.body.classList.add('loaded');
  const mySwiper = new Swiper('.swiper', {
    //effect: 'flip',
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
});
