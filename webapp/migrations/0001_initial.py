# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import jsonfield.fields
import webapp.models
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
                ('alto', models.PositiveIntegerField(null=True, blank=True)),
                ('ancho', models.PositiveIntegerField(null=True, blank=True)),
                ('num_paginas', models.PositiveIntegerField(null=True, blank=True)),
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
            name='Exposicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_inicial', models.DateTimeField()),
                ('fecha_final', models.DateTimeField(null=True, blank=True)),
                ('titulo', models.CharField(max_length=100)),
                ('subtitulo', models.CharField(max_length=100, blank=True)),
                ('creditos', models.TextField(blank=True)),
                ('descripcion', models.TextField(blank=True)),
                ('informacion', models.TextField(blank=True)),
                ('actividades', models.TextField(blank=True)),
                ('website', models.URLField(max_length=255, blank=True)),
                ('hashtag', models.CharField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('portada', models.ImageField(upload_to=webapp.models.get_exposicion_file_path)),
                ('categorias', models.ManyToManyField(to='webapp.Categoria')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('embed', models.TextField()),
                ('thumbnail', models.URLField(max_length=255, blank=True)),
                ('nombre', models.CharField(max_length=100, blank=True)),
                ('tipo', models.CharField(default=b'IMG', max_length=3, choices=[(b'IMG', b'Imagen'), (b'VID', b'Video'), (b'AUD', b'Audio')])),
                ('exposicion', models.ForeignKey(to='webapp.Exposicion')),
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
                ('website', models.URLField(max_length=255, blank=True)),
                ('twitter', models.URLField(max_length=255, blank=True)),
                ('facebook', models.URLField(max_length=255, blank=True)),
                ('youtube', models.URLField(max_length=255, blank=True)),
                ('instagram', models.URLField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('logotipo', models.ImageField(upload_to=webapp.models.get_museo_file_path)),
                ('portada', models.ImageField(upload_to=webapp.models.get_museo_file_path, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exposicion',
            name='museo',
            field=models.ForeignKey(to='webapp.Museo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogo',
            name='exposicion',
            field=models.ForeignKey(to='webapp.Exposicion'),
            preserve_default=True,
        ),
    ]
