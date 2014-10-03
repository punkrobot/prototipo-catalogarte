from django.shortcuts import render

from webapp.models import Museo

def index(request):
    return render(request, 'webapp/index.html')

def listado_museos(request):
    museos_list = Museo.objects.all()[:5]
    context = {'museos_list': museos_list}
    return render(request, 'webapp/museos.html', context)

def detalle_museo(request, museo_id):
    museo = get_object_or_404(Museo, pk = museo_id)
    context = {'museo': museo}
    return render(request, 'webapp/museo.html', context)
