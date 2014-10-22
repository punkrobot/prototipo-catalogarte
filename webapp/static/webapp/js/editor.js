$(function() {
    CKEDITOR.disableAutoInline = true;

    activarToolbar();
    activarAreasDeTexto();
    activarAreasDeContenido();

    inicializarModalMultimedia();
});

function agregarPagina(){
    var page = $("<div>", {class: "page"});
    var sel = $('input[type=radio]:checked').val();
    layout = $(sel).clone();
    layout.find('.area').addClass('content');
    page.html(layout.html());
    layout.remove();

    if(doc.numPaginas == 0){
        $("#workspace").html(page);
    } else {
        $("#workspace").append(page);
    }
    doc.numPaginas++;

    activarAreasDeContenido();
}

function activarAreasDeTexto(){
    $('.text').each(function() {
        generarAreaEditable($(this), $(this).html());
    });
}

function activarAreasDeContenido(){
    $(".content").droppable({
      hoverClass: "drop-active",
      drop: function( event, ui ) {
        if($(ui.draggable).hasClass("audio-video")){
            $(this).removeClass("area").addClass("video");

            var thumbnail = $('<div>', {class: 'video-thumbnail'});
            thumbnail.css('background-image', $(ui.draggable).css('background-image'));
            thumbnail.append('<div class="video-overlay"></div>');

            var footer = $('<div>', {class: 'footer'});
            footer.append($('<i>', {class: 'fa fa-video-camera'}));
            footer.append($(ui.draggable).attr("data-original-title"));

            $(this).append(thumbnail);
            $(this).append(footer);
        } else {
            $(this).removeClass("area").addClass("photo");
            $(this).css('background-image', $(ui.draggable).css('background-image'));
            $(this).backgroundDraggable();
        }
      }
    });

    $('.content').on("click", ".delete", eliminarContenido);
    $('.content').on("click", ".edit", editarContenido);

    $('.content').each(function() {
        agregarIconos($(this));
    });

    $('.photo').backgroundDraggable();
}

function eliminarContenido(){
    var content = $(this).parent();
    if(content.hasClass('photo')){
        content.removeAttr('style');
        content.removeClass('photo').addClass('area');
        content.find('.video-overlay').remove();
    } else if(content.hasClass('text')){
        content.find('.editable').remove();
        content.removeClass("text").addClass("area");
    } else if(content.hasClass('video')){
        content.find('.video-thumbnail').remove();
        content.find('.footer').remove();
        content.removeClass('video').addClass('area');
    }
}

function editarContenido() {
    var area = $(this).parent();
    area.removeClass("area").addClass("text");
    generarAreaEditable(area, '<h3>Encabezado</h3><p>Clic para editar el texto...</p>');
    agregarIconos(area);
}

function agregarIconos(area){
    area.append($("<i>", {class: "fa fa-edit fa-2x edit"}));
    area.append($("<i>", {class: "fa fa-times-circle fa-2x delete"}));
}
function generarAreaEditable(area, contenido){
    var editable = $('<div>', {class: 'editable', contenteditable: true});
    editable.html(contenido);
    area.html(editable);

    CKEDITOR.inline(editable.get(0), ckeditorConfigs.default);
}

function guardar(){
    $('.page').each(function(pageIndex) {
        var page = $(this).clone();
        page.hide();

        page.find('.edit').remove();
        page.find('.delete').remove();
        page.find('.text').each(function() {
            var editor = $(this).children(":first");
            $(this).html(editor.html());
        });

        var json = {
            'num': pageIndex,
            'html': page.html()
        }
        doc.paginas.push(json);

        page.remove();
    });

    $.ajax({
        type: 'POST',
        url: guardarUrl,
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

function cargarVideo(){
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

function cargarAudio(){
    var url = $('#audioUrlInput').val();
    if(url == ''){
        $('#audioUrlInputForm').addClass("has-error");
    } else {
        $('#audioUrlInputForm').removeClass("has-error");
        $('#audioLoadBtn').hide();
        $('#audio i').show();

        var oembed = 'https://soundcloud.com/oembed?format=json&maxheight=200&maxwidth=300&url=' + url;
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

function guardarAudio(){
    guardarRecurso({
        src : $('#audioPreview').html(),
        nombre : $('#audioPreview').data('title'),
        thumbnail : $('#audioPreview').data('thumbnail'),
        tipo : 'AUD'
    });
}

function guardarVideo(){
    guardarRecurso({
        src : $('#videoPreview').html(),
        nombre : $('#videoPreview').data('title'),
        thumbnail : $('#videoPreview').data('thumbnail'),
        tipo : 'VID'
    });
}

function guardarRecurso(media){
    $.ajax({
        type: 'POST',
        url: agregarMediaUrl,
        contentType: 'application/json; charset=utf-8',
        data: $.toJSON(media),
        success: function(data) {
            actualizarToolbar(data);
        }
    });
}

function cargarMultimedia(){
    $.ajax({
        type: 'GET',
        url: mediaUrl,
        contentType: 'text/html; charset=utf-8',
        success: function (data) {
            actualizarToolbar(data);
        }
    });
}

function actualizarToolbar(data){
    $("#multimediaToolbar").html(data);
    $('#multimediaModal').modal('hide');
    activarToolbar();
}

function activarToolbar(){
    $(".draggable").draggable({ opacity: 0.8, helper: "clone", appendTo:'body' });
    $(".audio-video").tooltip({container: 'body'});
}

function reiniciarModal(e) {
    $('#multimediaModal .fa-spin').hide();
    $('#videoLoadBtn').show();
    $('#videoInsertBtn').hide();
    $('#videoPreview').empty();
    $('#audioLoadBtn').show();
    $('#audioInsertBtn').hide();
    $('#audioPreview').empty();
}

function inicializarModalMultimedia(){
    $("#fileUploader").fineUploader({
        request: {
            endpoint: imgUploadUrl,
            forceMultipart: false,
            paramsInBody: false,
            customHeaders: {
                'X-CSRFToken': csrf,
            }
        }
    });
    $("#fileUploader").on("complete", function(event, id, name, response) {
        if (response.success) {
            cargarMultimedia();
        }
    });
    $('#multimediaModal').on('hidden.bs.modal', reiniciarModal);
}
