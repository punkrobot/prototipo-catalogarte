# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from autoslug import AutoSlugField
from jsonfield import JSONField
from datetimewidget.widgets import DateTimeWidget
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.signals import file_uploaded


def get_museo_file_path(instance, filename):
    return '/'.join([instance.slug, filename])

def get_exposicion_file_path(instance, filename):
    return '/'.join([instance.museo.slug, instance.slug, filename])


class Museo(models.Model):
    user = models.OneToOneField(User)

    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    detalles = models.TextField(blank=True)

    website = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    youtube = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)

    slug = AutoSlugField(unique=True, populate_from='nombre')
    logotipo = models.ImageField(upload_to=get_museo_file_path)
    portada = models.ImageField(upload_to=get_museo_file_path, blank=True)

    def __unicode__(self):
        return u'%s' % (self.nombre)


class Exposicion(models.Model):
    museo = models.ForeignKey(Museo)

    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)

    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100, blank=True)
    creditos = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)
    informacion = models.TextField(blank=True)
    actividades = models.TextField(blank=True)
    website = models.URLField(max_length=255, blank=True)
    hashtag = models.CharField(max_length=255, blank=True)

    slug = AutoSlugField(unique=True, populate_from='titulo')
    categorias = models.ManyToManyField("Categoria")
    portada = models.ImageField(upload_to=get_exposicion_file_path)

    def __unicode__(self):
        return u'%s - %s' % (self.museo.nombre, self.titulo)

    def get_categorias(self):
        categorias_list = self.categorias.values_list('nombre', flat=True)
        return ", ".join(categorias_list)

    def get_categorias_slugs(self):
        categorias_list = self.categorias.values_list('slug', flat=True)
        return " ".join(categorias_list)

    def get_imagenes(self):
        return self.media_set.filter(tipo=Media.IMAGEN)

    def get_videos(self):
        return self.media_set.filter(tipo=Media.VIDEO)

    def get_audios(self):
        return self.media_set.filter(tipo=Media.AUDIO)


class Catalogo(models.Model):
    exposicion = models.ForeignKey(Exposicion)

    alto = models.PositiveIntegerField(null=True, blank=True)
    ancho = models.PositiveIntegerField(null=True, blank=True)
    num_paginas = models.PositiveIntegerField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    publicado = models.NullBooleanField()

    contenido = JSONField(blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.museo.nombre, self.titulo)


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='nombre')

    def __unicode__(self):
        return u'%s' % (self.nombre)


class Media(models.Model):
    IMAGEN = 'IMG'
    VIDEO = 'VID'
    AUDIO = 'AUD'
    TIPOS = ( (IMAGEN, 'Imagen'), (VIDEO, 'Video'), (AUDIO, 'Audio') )

    exposicion = models.ForeignKey(Exposicion)

    url = models.TextField()
    embed = models.TextField()
    thumbnail = models.URLField(max_length=255, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(max_length=3, choices=TIPOS, default=IMAGEN)


@receiver(file_uploaded, sender=AjaxFileUploader)
def on_upload(sender, backend, request, **kwargs):
    Media.objects.create(url=request.GET['qqfilename'], exposicion_id=request.GET['exposicion_id'], tipo=Media.IMAGEN)

