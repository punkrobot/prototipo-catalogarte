var $container = $('#container');
$container.isotope({
    itemSelector: '.item',
    layoutMode: 'fitRows'
});
$('.filters-menu').on( 'click', 'li', function() {
    var filterValue = $(this).attr('data-filter');
    $container.isotope({ filter: filterValue });
});
$('#filters').on('affixed-top.bs.affix', function (e) {
    $('body').css("padding-top", "0");
})
$('#filters').on('affixed.bs.affix', function (e) {
    $('body').css("padding-top", "55px");
})
