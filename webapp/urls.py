from django.conf.urls import patterns, url

from webapp import views
from ajaxuploader.views import AjaxFileUploader

urlpatterns = patterns('',
    # auth urls:
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'webapp/auth/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/admin'}),

    # admin urls:
    url(r'^admin$', views.CatalogoAdmin.as_view(), name='catalogo_admin'),
    url(r'^admin/catalogo/nuevo$', views.CatalogoCreate.as_view(), name='catalogo_nuevo'),
    url(r'^admin/catalogo/contenido/(?P<slug>[\w-]+)/$', views.CatalogoCreateContent.as_view(), name='catalogo_contenido'),
    url(r'^admin/catalogo/(?P<slug>[\w-]+)/$', views.CatalogoUpdate.as_view(), name='catalogo_actualizar'),

    # public urls:
    url(r'^$', views.CatalogoList.as_view(), name='catalogo_lista'),
    url(r'^catalogo/(?P<slug>[\w-]+)/$', views.CatalogoDetail.as_view(), name='catalogo_detalle'),

    url(r'^ajax-upload$', AjaxFileUploader(), name="ajax_upload"),
)
