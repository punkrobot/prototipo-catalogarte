from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from webapp.models import Museo, Catalogo
from webapp.forms import CatalogoForm

class CatalogoList(ListView):
    context_object_name = 'catalogo_list'
    template_name = 'webapp/catalogo_list.html'

    def get_queryset(self):
        return Catalogo.objects.all()


class CatalogoDetail(DetailView):
    model = Catalogo
    context_object_name = 'catalogo'
    template_name = 'webapp/catalogo_detail.html'

    def get_object(self):
        return get_object_or_404(Catalogo, slug=self.kwargs.get('slug', None))


class CatalogoAdmin(LoginRequiredMixin, ListView):
    context_object_name = 'catalogo_list'
    template_name = 'webapp/admin/catalogo_admin.html'

    def get_queryset(self):
        return Catalogo.objects.filter(museo__id=self.request.user.museo.id)


class CatalogoCreate(LoginRequiredMixin, CreateView):
    form_class = CatalogoForm
    template_name = 'webapp/admin/catalogo_form.html'
    success_url = '/admin'

    def form_valid(self, form):
        form.instance.museo = self.request.user.museo
        return super(CatalogoCreate, self).form_valid(form)


class CatalogoUpdate(UpdateView):
    model = Catalogo
    form_class = CatalogoForm
    template_name = 'webapp/admin/catalogo_form.html'
    success_url = '/admin'


