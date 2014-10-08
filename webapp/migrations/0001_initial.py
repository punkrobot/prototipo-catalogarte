# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_inicial', models.DateTimeField()),
                ('fecha_final', models.DateTimeField(null=True, blank=True)),
                ('titulo', models.CharField(max_length=100)),
                ('autor', models.CharField(max_length=100, blank=True)),
                ('creditos', models.TextField(blank=True)),
                ('informacion', models.TextField(blank=True)),
                ('actividades', models.TextField(blank=True)),
                ('website', models.URLField(max_length=100, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('portada', models.ImageField(upload_to=b'')),
                ('num_paginas', models.IntegerField(null=True, blank=True)),
                ('fecha_publicacion', models.DateTimeField(null=True, blank=True)),
                ('fecha_modificacion', models.DateTimeField(null=True, blank=True)),
                ('publicado', models.NullBooleanField()),
                ('contenido', jsonfield.fields.JSONField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField()),
                ('detalles', models.TextField(blank=True)),
                ('website', models.URLField(max_length=100, blank=True)),
                ('twitter', models.URLField(max_length=100, blank=True)),
                ('facebook', models.URLField(max_length=100, blank=True)),
                ('youtube', models.URLField(max_length=100, blank=True)),
                ('instagram', models.URLField(max_length=100, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('logotipo', models.ImageField(upload_to=b'')),
                ('portada', models.ImageField(upload_to=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='catalogo',
            name='categorias',
            field=models.ManyToManyField(to='webapp.Categoria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogo',
            name='museo',
            field=models.ForeignKey(to='webapp.Museo'),
            preserve_default=True,
        ),
    ]
