# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='descripcion',
            field=models.TextField(default='Yayoi Kusama. Obsesi\xf3n Infinita es la primera muestra retrospectiva en Am\xe9rica Latina de una de las artistas japonesas m\xe1s relevantes de nuestro tiempo. La exposici\xf3n presenta un recorrido exhaustivo a trav\xe9s de m\xe1s de 100 obras creadas entre 1950 y 2013, que incluyen pinturas, trabajos en papel, esculturas, videos, slideshows e instalaciones. Se presenta la trayectoria de la artista desde el \xe1mbito privado a la esfera p\xfablica, desde la pintura al performance, del estudio a la calle.', blank=True),
            preserve_default=False,
        ),
    ]
