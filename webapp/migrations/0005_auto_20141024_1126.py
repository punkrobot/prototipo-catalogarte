# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20141014_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='src',
            new_name='embed',
        ),
        migrations.AddField(
            model_name='media',
            name='url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
