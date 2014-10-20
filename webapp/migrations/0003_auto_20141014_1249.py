# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20141013_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='ruta',
        ),
        migrations.AddField(
            model_name='media',
            name='src',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
