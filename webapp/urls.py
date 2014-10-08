from django.conf.urls import patterns, url

from webapp import views

urlpatterns = patterns('',
    # auth urls:
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'webapp/auth/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/admin'}),

    # admin urls:
    url(r'^admin$', views.CatalogoAdmin.as_view(), name='catalogo_admin'),
    url(r'^admin/catalogo/nuevo$', views.CatalogoCreate.as_view(), name='catalogo_nuevo'),

    # public urls:
    url(r'^$', views.CatalogoList.as_view(), name='catalogo_lista'),
)
