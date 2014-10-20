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

    $(".audio-video").tooltip({container: 'body'});
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
        if($(ui.draggable).hasClass("audio-video")){
            $(this).removeClass("area").addClass("photo");
            $(this).css('background-image', $(ui.draggable).css('background-image'));
            $(this).append('<div class="video-overlay"></div>');
        } else {
            $(this).removeClass("area").addClass("photo");
            $(this).css('background-image', $(ui.draggable).css('background-image'));
        }
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

function loadVideo(){
	var url = $('#videoUrlInput').val();
	if(url == ''){
		$('#videoUrlInputForm').addClass("has-error");
	} else {
		$('#videoUrlInputForm').removeClass("has-error");
		$('#videoLoadBtn').hide();
		$('#video i').show();

		var oembed = 'http://www.youtube.com/oembed?format=json&url=' + url;
		$.ajax({
			url: 'http://query.yahooapis.com/v1/public/yql',
            data: {
                q: "select * from json where url ='" + oembed + "'",
                format: "json"
            },
            dataType: "jsonp",
            success: function (data) {
                $('#video i').hide();
                $('#videoInsertBtn').show();
                $('#videoPreview').data('title', data.query.results.json.title);
                $('#videoPreview').data('thumbnail', data.query.results.json.thumbnail_url);
                $('#videoPreview').html(data.query.results.json.html);
                $('#videoPreview').show();
            },
            error: function (result) {
                console.log("Error", result);
            }
    	});
	}
}

function loadAudio(){
    var url = $('#audioUrlInput').val();
    if(url == ''){
        $('#audioUrlInputForm').addClass("has-error");
    } else {
        $('#audioUrlInputForm').removeClass("has-error");
        $('#audioLoadBtn').hide();
        $('#audio i').show();

        var oembed = 'https://soundcloud.com/oembed?format=json&url=' + url;
        $.ajax({
            url: oembed,
            dataType: "json",
            success: function (data) {
                $('#audio i').hide();
                $('#audioInsertBtn').show();
                $('#audioPreview').data('title', data.title);
                $('#audioPreview').data('thumbnail', data.thumbnail_url);
                $('#audioPreview').html(data.html);
                $('#audioPreview').show();
            },
            error: function (result) {
                console.log("Error", result);
            }
        });
    }
}

function saveAudio(){
    saveMedia({
        src : $('#audioPreview').html(),
        nombre : $('#audioPreview').data('title'),
        thumbnail : $('#audioPreview').data('thumbnail'),
        tipo : 'AUD'
    });
}

function saveVideo(){
    saveMedia({
        src : $('#videoPreview').html(),
        nombre : $('#videoPreview').data('title'),
        thumbnail : $('#videoPreview').data('thumbnail'),
        tipo : 'VID'
    });
}

function saveMedia(media){
    $.ajax({
        type: 'POST',
        url: media_url,
        contentType: 'application/json; charset=utf-8',
        data: $.toJSON(media),
        dataType: 'json',
        success: function (data) {
            console.log("Success");
        },
        error: function(data) {
            console.log("Error");
        }
    });
}
