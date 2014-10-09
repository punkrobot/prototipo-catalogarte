# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_catalogo_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
        ),
    ]
