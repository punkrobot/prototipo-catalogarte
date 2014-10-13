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
    url(r'^admin/exposicion/catalogo/(?P<slug>[\w-]+)/$', views.CatalogoCreate.as_view(), name='catalogo_create'),
    url(r'^admin/exposicion/(?P<slug>[\w-]+)/$', views.ExposicionUpdate.as_view(), name='exposicion_actualizar'),
    url(r'^admin/catalogo/save/(?P<slug>[\w-]+)/$', views.CatalogoSave.as_view(), name='catalogo_save'),

    # public urls:
    url(r'^$', views.ExposicionList.as_view(), name='exposicion_lista'),
    url(r'^exposicion/(?P<slug>[\w-]+)/$', views.ExposicionDetail.as_view(), name='exposicion_detalle'),
    url(r'^media_upload$', AjaxFileUploader(), name="ajax_upload"),
)
