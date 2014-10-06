from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Museo, Catalogo

def index(request):
    return render(request, 'webapp/index.html')

class CatalogoList(ListView):
    context_object_name = 'catalogo_list'
    template_name = 'webapp/catalogo_list.html'

    def get_queryset(self):
        return Catalogo.objects.filter(museo__id=self.request.user.museo.id)

class CatalogoCreate(CreateView):
    model = Catalogo
    success_url = '/admin'


def listado_museos(request):
    museos_list = Museo.objects.all()[:5]
    context = {'museos_list': museos_list}
    return render(request, 'webapp/museos.html', context)

def detalle_museo(request, museo_id):
    museo = get_object_or_404(Museo, pk = museo_id)
    context = {'museo': museo}
    return render(request, 'webapp/museo.html', context)
