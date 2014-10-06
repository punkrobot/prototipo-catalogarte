from django.conf.urls import patterns, url

from webapp import views

urlpatterns = patterns('',
    # auth urls:
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'webapp/auth/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/admin'}),

    # admin urls:
    url(r'^admin$', views.CatalogoList.as_view()),
    url(r'^admin/catalogo/nuevo$', views.CatalogoCreate.as_view()),

    # public urls:
    url(r'^$', views.index, name='index'),
    url(r'^museos$', views.listado_museos, name='listado_museos'),
    url(r'^museo/(?P<museo_id>\d+)$', views.detalle_museo, name='detalle_museo'),
)
