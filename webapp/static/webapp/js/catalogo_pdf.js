$(function() {
    for(i=0; i<catalogo.paginas.paginas.length; i++){
        var pagina = catalogo.paginas.paginas[i];
        if(pagina.nombre != ''){
            $('.contenido').css('display', 'inline-block');

            var a = $('<a>', { html: pagina.nombre });
            a.on('click', {n: i+1}, function (e) {
                $(".flipbook").turn("page", e.data.n);
            });

            $('.contenido ul').append($('<li>').append(a));
        }
    }

    $('.flipbook').turn({autoCenter:true, gradients: true, acceleration: true});

    $('.flipbook .next').click(function(){
      $('.flipbook').turn('next');
    });
    $('.flipbook .prev').click(function(){
      $('.flipbook').turn('previous');
    });

    $('.foto img, .content.fondo').click(function() {
      var img = $(this);
      var url = '';
      if(img.hasClass('fondo')){
        url = /^url\((['"]?)(.*)\1\)$/.exec(img.css('background-image'));
        url = url ? url[2] : '';
      } else {
        url = img.attr('src');
      }

      $.magnificPopup.open({
        items: {
          src: url
        },
        type: 'image',
        mainClass: 'mfp-no-margins mfp-with-zoom',
        closeOnContentClick: true,

        zoom: {
          enabled: true,
          duration: 300,
          easing: 'ease-in-out',

          opener: function(openerElement) {
            return img;
          }
        }
      }, 0);
    });

    $('.video>a').magnificPopup({
      disableOn: 700,
      type: 'iframe',
      mainClass: 'mfp-fade',
      removalDelay: 160,
      preloader: false,

      fixedContentPos: false
    });
});
