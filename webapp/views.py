import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views.generic import View, CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from webapp.models import Museo, Exposicion, Catalogo
from webapp.forms import ExposicionForm


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
        # TODO: Revisar error
        return reverse('catalogo_create', args=(self.object.slug))


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


class CatalogoSave(CsrfExemptMixin, View):
    def post(self, request, slug):
        if request.is_ajax():
            if request.method == 'POST':
                exposicion = get_object_or_404(Exposicion, slug=slug)
                catalogo = exposicion.catalogo_set.first()
                catalogo.contenido = json.loads(request.body)
                catalogo.save()

                return HttpResponse('ok')


class ExposicionUpdate(UpdateView):
    model = Exposicion
    form_class = ExposicionForm
    template_name = 'webapp/admin/exposicion_form.html'
    success_url = '/admin'


