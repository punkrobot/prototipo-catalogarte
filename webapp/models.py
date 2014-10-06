# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.forms import MultipleChoiceField

from autoslug import AutoSlugField
from jsonfield import JSONField

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

class Catalogo(models.Model):
    museo = models.ForeignKey(Museo)

    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)

    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, blank=True)
    creditos = models.TextField(blank=True)
    informacion = models.TextField(blank=True)
    actividades = models.TextField(blank=True)
    website = models.URLField(max_length=100, blank=True)

    slug = AutoSlugField(populate_from='titulo')
    portada = models.ImageField()

    CATEGORIAS_CHOICES = (
        ('AP', 'Artes plásticas'),
        ('AV', 'Artes visuales'),
        ('F', 'Fotografía'),
        ('C', 'Ciencia'),
        ('I', 'Infantil'),
    )
    categorias = MultipleChoiceField(choices=CATEGORIAS_CHOICES)

    num_paginas = models.IntegerField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    publicado = models.NullBooleanField()

    contenido = JSONField(blank=True)
