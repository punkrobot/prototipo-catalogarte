$(function() {
    var options = {
        horizontal: 1,
        itemNav: 'forceCentered',
        activateMiddle: 1,
        speed: 300,
        scrollBy: 1,
        touchDragging: 1,
        scrollBar: '.scrollbar',
    };

    var frame = new Sly('.frame', options).init();

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
