from django.conf.urls import patterns, url

from webapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^museos$', views.listado_museos, name='listado_museos'),
    url(r'^museo/(?P<museo_id>\d+)$', views.detalle_museo, name='detalle_museo'),
)
