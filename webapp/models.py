from django.db import models

from django.contrib.auth.models import User

class Museo(models.Model):
    user = models.OneToOneField(User)

    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    #email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    horarios = models.CharField(max_length=100, blank=True)

    website = models.URLField(max_length=100)
    twitter = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)

    logotipo = models.ImageField()
