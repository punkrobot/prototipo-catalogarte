import codecs
import json
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin, AjaxResponseMixin

from webapp.forms import ExposicionForm, MuseoForm
from webapp.models import Museo, Exposicion, Catalogo, Media


class MuseoAdmin(LoginRequiredMixin, ListView):
    context_object_name = 'museo_list'
    template_name = 'webapp/admin/museo_admin.html'

    def get_queryset(self):
        return Museo.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')
        elif request.user.is_staff:
            return super(MuseoAdmin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('exposicion_admin')


class ExposicionList(ListView):
    context_object_name = 'exposicion_list'
    template_name = 'webapp/exposicion_list.html'

    def get_queryset(self):
        return Exposicion.objects.all()


class ExposicionDetail(DetailView):
    model = Exposicion
    context_object_name = 'exposicion'
    template_name = 'webapp/exposicion_detail.html'

    def get_object(self):
        return get_object_or_404(Exposicion, slug=self.kwargs.get('slug', None))


class ExposicionAdmin(LoginRequiredMixin, ListView):
    context_object_name = 'exposicion_list'
    template_name = 'webapp/admin/exposicion_admin.html'

    def get_queryset(self):
        return Exposicion.objects.filter(museo__id=self.request.user.museo.id)


class ExposicionCreate(LoginRequiredMixin, CreateView):
    form_class = ExposicionForm
    template_name = 'webapp/admin/exposicion_form.html'

    def form_valid(self, form):
        form.instance.museo = self.request.user.museo
        return super(ExposicionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('catalogo_create', kwargs={'slug' : self.object.slug } )


class ExposicionUpdate(LoginRequiredMixin, UpdateView):
    model = Exposicion
    form_class = ExposicionForm
    template_name = 'webapp/admin/exposicion_form.html'
    success_url = '/admin'


class CatalogoDetail(View):
    def get(self, request, slug, tipo):
        exposicion = get_object_or_404(Exposicion, slug=slug)
        catalogo =  exposicion.catalogo_set.first()
        contenido = json.dumps(catalogo.contenido)

        template = 'webapp/catalogo_detail.html' if tipo == 'html' else 'webapp/catalogo_detail_pdf.html'

        context = {
            'exposicion': exposicion,
            'catalogo': catalogo,
            'contenido': contenido
        }
        return render(request, template, context)


class CatalogoCreate(LoginRequiredMixin, View):
    def get(self, request, slug):
        exposicion = get_object_or_404(Exposicion, slug=slug)
        catalogos = Catalogo.objects.filter(exposicion__id=exposicion.id)
        if catalogos.exists():
            catalogo = catalogos.first()
        else:
            catalogo = Catalogo(
                exposicion=exposicion,
                ancho=710, alto=580,
                num_paginas=0,
                publicado=False,
                fecha_modificacion=datetime.now() )
            catalogo.save()

        context = {
            'csrf_token': get_token(request),
            'ckeditor_configs': settings.CKEDITOR_CONFIGS,
            'exposicion': exposicion,
            'catalogo': catalogo
        }
        return render(request, 'webapp/admin/catalogo_create.html', context)


class CatalogoSave(LoginRequiredMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, slug):
        exposicion = get_object_or_404(Exposicion, slug=slug)
        catalogo = exposicion.catalogo_set.first()
        catalogo.contenido = json.loads(request.body)
        catalogo.save()

        return HttpResponse('ok')


class CatalogoExport(LoginRequiredMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, slug):
        exposicion = get_object_or_404(Exposicion, slug=slug)
        catalogo = exposicion.catalogo_set.first()

        template = 'webapp/admin/print.html'
        context = { 'document' : json.loads(request.body) }

        path = 'media/' + request.user.museo.slug + '/' + exposicion.slug + '/';

        codecs.open(path + 'catalogo.html', 'w', 'utf-8').write(render_to_string(template, context))

        address = 'http://localhost:8000/' + path + 'catalogo.html'
        pdf_file = path + 'catalogo.pdf'
        external_process = Popen(["phantomjs", "phantom.js", address, pdf_file], stdout=PIPE, stderr=STDOUT)
        external_process.communicate()

        response_data = {
            'file': '/' + pdf_file
        }

        return HttpResponse(json.dumps(response_data), content_type="application/json")


class MuseoCreate(LoginRequiredMixin, CreateView):
    form_class = MuseoForm
    template_name = 'webapp/admin/museo_form.html'
    success_url = '/admin'


class MuseoDetail(DetailView):
    model = Museo
    context_object_name = 'museo'
    template_name = 'webapp/museo_detail.html'

    def get_object(self):
        return get_object_or_404(Museo, slug=self.kwargs.get('slug', None))


class MediaList(LoginRequiredMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, slug):
        context = {
            'exposicion': get_object_or_404(Exposicion, slug=slug)
        }
        return render(request, 'webapp/admin/multimedia_toolbar.html', context)


class MediaCreate(LoginRequiredMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, slug):
        exposicion = get_object_or_404(Exposicion, slug=slug)
        media_json = json.loads(request.body)

        media = Media(
            exposicion=exposicion,
            thumbnail=media_json['thumbnail'],
            nombre=media_json['nombre'],
            tipo=media_json['tipo'],
            url=media_json['url'],
            embed=media_json['embed'] )
        media.save()

        context = {
            'exposicion': get_object_or_404(Exposicion, slug=slug)
        }

        return render(request, 'webapp/admin/multimedia_toolbar.html', context)



