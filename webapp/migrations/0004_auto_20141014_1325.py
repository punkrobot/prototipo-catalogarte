# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20141014_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='thumbnail',
            field=models.URLField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exposicion',
            name='website',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='facebook',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='instagram',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='twitter',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='website',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='youtube',
            field=models.URLField(max_length=255, blank=True),
        ),
    ]
