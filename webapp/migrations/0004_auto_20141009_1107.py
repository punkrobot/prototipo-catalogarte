# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20141008_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='portada',
            field=models.ImageField(upload_to=webapp.models.get_catalogo_file_path),
        ),
        migrations.AlterField(
            model_name='museo',
            name='logotipo',
            field=models.ImageField(upload_to=webapp.models.get_museo_file_path),
        ),
        migrations.AlterField(
            model_name='museo',
            name='portada',
            field=models.ImageField(upload_to=webapp.models.get_museo_file_path, blank=True),
        ),
    ]
