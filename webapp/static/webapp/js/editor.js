$(function() {
    CKEDITOR.disableAutoInline = true;

    activarToolbar();
    activarAreasDeTexto();
    activarAreasDeContenido();

    inicializarModalMultimedia();

    cargaDocumento();

    $('body').scrollspy({ target: '#toolbar-documento', offset: 150 });
});

function cargaDocumento(){
    if(doc.numPaginas > 0){
        var lista = $('#toolbar-documento ul');

        actualizarDocumento();

        for(i=0; i<doc.numPaginas; i++){
            agregarPaginaNav(i, doc.paginas[i].id, doc.paginas[i].nombre, lista);
        }
    }
}

function agregarPaginaNav(index, id, titulo, container){
    if(index == 0){
        container.empty();
    }

    var li = $('<li>', {class: index == 0 ? 'active' : ''});
    li.data('src', '#' + id);
    var pagina = $('<a>', {href: '#' + id});
    li.append(pagina);

    var nombre = $('<span>');
    nombre.html(titulo);
    nombre.editable({ container: 'body', title: 'Nombre de la hoja:', placement: 'right', toggle: 'manual', defaultValue: '', emptytext: '&nbsp;' });
    nombre.on('save', function(e, params) {
        var id = $(e.target).parent().attr('href');
        $(id).attr('title', params.newValue);
    });
    pagina.append(nombre);

    var eliminarIcono = $('<i>', {class: 'fa fa-remove pull-right'});
    eliminarIcono.click(function(e){
        bootbox.confirm("¿Estás seguro de borrar la página?", function(result) {
            if(result){
                var id = $(e.target).parent().attr('href');
                $(id).remove();
                $(e.target).parent().parent().remove();
                doc.numPaginas--;
            }
        });

        e.preventDefault();
    });
    var editarIcono = $('<i>', {class: 'fa fa-pencil pull-right'});
    editarIcono.click(function(e){
        e.stopPropagation();
        e.preventDefault();
        $(e.target).prev().prev().editable('toggle');
    });
    pagina.append(eliminarIcono);
    pagina.append(editarIcono);

    container.append(li);
}

function agregarPagina(){
    var idPagina = 'pag'+ doc.sigId;
    var nombrePagina = 'Página '+ (doc.numPaginas+1);

    var page = $("<div>", {class: "page", id: idPagina, title: nombrePagina});

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

    activarAreasDeContenido();

    agregarPaginaNav(doc.numPaginas, "pag"+doc.sigId, nombrePagina, $('#toolbar-documento ul'));

    $('[data-spy="scroll"]').each(function () {
      var $spy = $(this).scrollspy('refresh')
    });

    doc.sigId++;
    doc.numPaginas++;
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
        if($(ui.draggable).hasClass("pre-video")){
            $(this).removeClass("area").addClass("video");

            var link = $('<a>', {href: $(ui.draggable).data('url'), target: '_blank'});

            var thumbnail = $('<div>', {class: 'video-thumbnail'});
            thumbnail.css('background-image', $(ui.draggable).css('background-image'));
            thumbnail.append('<div class="video-overlay"></div>');

            var footer = $('<div>', {class: 'footer'});
            footer.append($('<i>', {class: 'fa fa-video-camera'}));
            footer.append($(ui.draggable).attr("data-original-title"));

            link.append(thumbnail);
            $(this).append(link);
            $(this).append(footer);

        }else if($(ui.draggable).hasClass("pre-audio")){
            $(this).removeClass("area").addClass("audio");
            $(this).append($(ui.draggable).data('html'));

            var footer = $('<div>', {class: 'footer'});
            footer.append($('<i>', {class: 'fa fa-music'}));
            footer.append($(ui.draggable).attr("data-original-title"));

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
        content.find('.text-editable').remove();
        content.removeClass("text").addClass("area");
    } else if(content.hasClass('video')){
        content.find('a').remove();
        content.find('.footer').remove();
        content.removeClass('video').addClass('area');
    } else if(content.hasClass('audio')){
        content.find('iframe').remove();
        content.find('.footer').remove();
        content.removeClass('audio').addClass('area');
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
    var editable = $('<div>', {class: 'text-editable', contenteditable: true});
    editable.html(contenido);
    area.html(editable);

    CKEDITOR.inline(editable.get(0), ckeditorConfigs.default);
}

function actualizarDocumento(){
    doc.paginas = [];

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
            'id': page.attr('id'),
            'nombre': page.attr('title'),
            'html': page.cleanWhitespace().html()
        }
        doc.paginas.push(json);

        page.remove();
    });
}

function guardar(){
    var cargando = $(".list-group .list-group-item i.fa-spin");
    cargando.show();

    actualizarDocumento();
    $.ajax({
        type: 'POST',
        url: guardarUrl,
        contentType: 'application/json; charset=utf-8',
        data: $.toJSON(doc),
        dataType: 'text',
        success: function (data) {
            cargando.hide();
            var alerta = $('<div class="alert alert-dismissable alert-message" style="display: none;">');
            alerta.append($('<button type="button" class="close" data-dismiss="alert">&times</button>'));
            alerta.append("Catálogo guardado correctamente");
            alerta.appendTo($('body')).fadeIn(500).delay(2000).fadeOut(500);
        },
        error: function(data) {
            console.log("Error");
        }
    });
}

function exportar(){
    actualizarDocumento();
    $.ajax({
        type: 'POST',
        url: exportarUrl,
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
                $('#videoPreview').data('url', 'https://www.youtube.com/watch?v='+url.split("v=")[1].substring(0, 11));
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

        var oembed = 'https://soundcloud.com/oembed?format=json&maxheight=230&url=' + url;
        $.ajax({
            url: oembed,
            dataType: "json",
            success: function (data) {
                $('#audio i').hide();
                $('#audioInsertBtn').show();
                $('#audioPreview').data('url', url);
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
        url : $('#audioPreview').data('url'),
        embed : $('#audioPreview').html(),
        nombre : $('#audioPreview').data('title'),
        thumbnail : $('#audioPreview').data('thumbnail'),
        tipo : 'AUD'
    });
}

function guardarVideo(){
    guardarRecurso({
        url : $('#videoPreview').data('url'),
        embed : $('#videoPreview').html(),
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
    $(".pre-video").tooltip({container: 'body'});
    $(".pre-audio").tooltip({container: 'body'});
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

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

jQuery.fn.cleanWhitespace = function() {
    this.contents().filter(function() {
        if (this.nodeType != 3) {
            $(this).cleanWhitespace();
            return false;
        } else {
            this.textContent = $.trim(this.textContent);
            return !/\S/.test(this.nodeValue);
        }
    }).remove();
    return this;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    }
});
