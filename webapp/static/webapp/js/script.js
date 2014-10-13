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




$(function() {
    CKEDITOR.disableAutoInline = true;

    $( ".draggable" ).draggable({ opacity: 0.8, helper: "clone", appendTo:'body' });
    activateContentAreas();
    activateTextAreas();
});

function addPage(){
    var page = $("<div>", {class: "page"});

    var sel = $('input[type=radio]:checked').val();
    var layoutJson = {};
    var layout;
    if(sel == 1){
        layout = $('#layout1').clone();
    } else if(sel == 2){
        layout = $('#layout2').clone();
    } else if(sel == 3){
        layout = $('#layout3').clone();
    } else {
        layout = $('#layout4').clone();
    }
    page.append(layout);

    if(doc.numPages == 0){
        $("#workspace").html(page);
    } else {
        $("#workspace").append(page);
    }
    doc.numPages++;

    activateContentAreas();
}

function activateTextAreas(){
    $('.editable').each(function() {
        CKEDITOR.inline($(this).get(0), ckeditor_configs.default);
    });
}

function activateContentAreas(){
    $(".droppable").droppable({
      drop: function( event, ui ) {
        $(this).removeClass("area").addClass("photo");
        $(this).css('background-image', $(ui.draggable).css('background-image'));
      }
    });

    $('.content').on("click", ".delete", function() {
        var content = $(this).parent();
        if(content.hasClass('photo')){
            content.css('background-image', 'none');
            content.removeClass('photo').addClass('area');
        } else if(content.hasClass('text')){
            content.remove('.editable');
            content.removeClass("text").addClass("area");
        }
    });

    $('.content').on("click", ".edit", function() {
        var area = $(this).parent();
        area.removeClass("area").addClass("text");

        var editable = $('<div>', {id: 'editor1', class: 'editable', contenteditable: true});
        editable.html('<h3>Encabezado</h3><p>Clic para editar el texto...</p>');
        area.append(editable);

        CKEDITOR.inline(editable.get(0), ckeditor_configs.default);
    });
}

function save(){
    $('.page').each(function(pageIndex) {
        var page = {
            'num': pageIndex,
            rows: []
        }

        $(this).find('.r').each(function(rowIndex) {
            var row = {
                'class': $(this).attr('class'),
                cols: []
            }

            $(this).find('.c').each(function(colIndex) {
                var col = {
                    'class': $(this).attr('class')
                };
                var content = $(this).children('.content').first();
                if(content.hasClass('photo')){
                    col.content = {
                        'type': 'photo',
                        'src': content.css('background-image')
                    }
                } else if(content.hasClass('text')){
                    var html = content.children('.editable').html();
                    col.content = {
                        'type': 'text',
                        'html': html
                    }
                } else if(content.hasClass('area')){
                    console.log("Empty area");
                }
                row.cols.push(col);
            });
            page.rows.push(row);
        });
        doc.pages.push(page);
    });

    $.ajax({
        type: 'POST',
        url: save_url,
        contentType: 'application/json; charset=utf-8',
        data: $.toJSON(doc),
        dataType: 'text',
        success: function (data) {
            console.log("Success");
        },
        error: function(data) {
            console.log("Error");
        }
    });
}

