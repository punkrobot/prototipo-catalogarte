# -*- coding: utf-8 -*-

from django import forms

from datetimewidget.widgets import DateTimeWidget
from ckeditor.widgets import CKEditorWidget

from webapp.models import Exposicion

class ExposicionForm(forms.ModelForm):

    class Meta:
        model = Exposicion
        fields = ['titulo', 'subtitulo', 'fecha_inicial', 'fecha_final', 'descripcion', 'creditos', \
                  'informacion', 'actividades', 'categorias', 'website', 'hashtag', 'portada']

        success_url = '/admin'

    def __init__(self, *args, **kwargs):
        super(ExposicionForm, self).__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs = {'placeholder': 'Nombre de la exposición'}
        self.fields['subtitulo'].widget.attrs = {'placeholder': 'Subtitulo o autor de la exposición'}
        self.fields['fecha_inicial'].widget = DateTimeWidget(usel10n=True, bootstrap_version=3)
        self.fields['fecha_final'].widget = DateTimeWidget(usel10n=True, bootstrap_version=3)
        self.fields['descripcion'].widget.attrs = {'placeholder': 'Descripción corta de la exposición...', 'rows': 4}
        self.fields['creditos'].widget = CKEditorWidget()
        self.fields['creditos'].initial = '<h3>Curaduría</h3><ul><li></li></ul>'
        self.fields['informacion'].widget = CKEditorWidget()
        self.fields['informacion'].initial = '<h3>Horarios</h3><ul><li></li><li></li></ul><hr><h3>Precios</h3><ul><li></li><li></li></ul>'
        self.fields['actividades'].widget = CKEditorWidget()
        self.fields['actividades'].initial = '<h3>Actividades</h3><ul><li></li><li></li></ul><hr><h3>Talleres</h3><ul><li></li><li></li></ul>'
        self.fields['website'].widget.attrs = {'placeholder': ''}
        self.fields['hashtag'].widget.attrs = {'placeholder': '#HastagDeLaExposicion'}
