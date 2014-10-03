from django.db import models

from django.contrib.auth.models import User

class Museo(models.Model):
    user = models.OneToOneField(User)

    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    logotipo = models.ImageField()
    telefono = models.CharField(max_length=100)
    horarios = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    twitter = models.URLField(max_length=100)
    facebook = models.URLField(max_length=100)

