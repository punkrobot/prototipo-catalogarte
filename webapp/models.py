# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from autoslug import AutoSlugField
from jsonfield import JSONField
from datetimewidget.widgets import DateTimeWidget

class Museo(models.Model):
    user = models.OneToOneField(User)

    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    #email = models.EmailField(blank=True)
    detalles = models.TextField(blank=True)

    website = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    youtube = models.URLField(max_length=100, blank=True)
    instagram = models.URLField(max_length=100, blank=True)

    slug = AutoSlugField(populate_from='nombre')
    logotipo = models.ImageField()
    portada = models.ImageField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.nombre)

class Catalogo(models.Model):
    museo = models.ForeignKey(Museo)

    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)

    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, blank=True)
    creditos = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)
    informacion = models.TextField(blank=True)
    actividades = models.TextField(blank=True)
    website = models.URLField(max_length=100, blank=True)

    slug = AutoSlugField(unique=True, populate_from='titulo')
    categorias = models.ManyToManyField("Categoria")
    portada = models.ImageField()

    num_paginas = models.IntegerField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    publicado = models.NullBooleanField()

    contenido = JSONField(blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.museo.nombre, self.titulo)

    def get_categorias(self):
        categorias_list = self.categorias.values_list('nombre', flat=True)
        return ", ".join(categorias_list)

    def get_categorias_slugs(self):
        categorias_list = self.categorias.values_list('slug', flat=True)
        return " ".join(categorias_list)

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='nombre')

    def __unicode__(self):
        return u'%s' % (self.nombre)

