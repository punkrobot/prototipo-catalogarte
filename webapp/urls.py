from django.conf.urls import patterns, url

from webapp import views
from ajaxuploader.views import AjaxFileUploader

urlpatterns = patterns('',
    # auth urls:
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'webapp/auth/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/admin'}),

    # admin urls:
    url(r'^admin$', views.ExposicionAdmin.as_view(), name='exposicion_admin'),
    url(r'^admin/exposicion/nueva$', views.ExposicionCreate.as_view(), name='exposicion_nueva'),
    url(r'^admin/exposicion/(?P<slug>[\w-]+)/$', views.ExposicionUpdate.as_view(), name='exposicion_actualizar'),
    url(r'^admin/exposicion/(?P<slug>[\w-]+)/media/img$', AjaxFileUploader(), name='img_agregar'),
    url(r'^admin/exposicion/(?P<slug>[\w-]+)/media/agregar$', views.MediaCreate.as_view(), name='media_agregar'),
    url(r'^admin/exposicion/(?P<slug>[\w-]+)/media$', views.MediaList.as_view(), name='media_list'),

    url(r'^admin/catalogo/(?P<slug>[\w-]+)/$', views.CatalogoCreate.as_view(), name='catalogo_create'),
    url(r'^admin/catalogo/(?P<slug>[\w-]+)/save/$', views.CatalogoSave.as_view(), name='catalogo_save'),
    url(r'^admin/catalogo/(?P<slug>[\w-]+)/export/$', views.CatalogoExport.as_view(), name='catalogo_export'),

    # public urls:
    url(r'^$', views.ExposicionList.as_view(), name='exposicion_lista'),
    url(r'^exposicion/(?P<slug>[\w-]+)/$', views.ExposicionDetail.as_view(), name='exposicion_detalle'),
    url(r'^exposicion/(?P<slug>[\w-]+)/catalogo/$', views.CatalogoDetail.as_view(), name='catalogo_detalle'),
)
