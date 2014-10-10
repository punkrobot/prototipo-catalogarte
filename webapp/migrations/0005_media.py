# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20141009_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.CharField(max_length=255)),
                ('catalogo', models.ForeignKey(to='webapp.Catalogo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
