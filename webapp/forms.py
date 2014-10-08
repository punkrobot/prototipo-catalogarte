# -*- coding: utf-8 -*-

from django import forms

from datetimewidget.widgets import DateTimeWidget
from ckeditor.widgets import CKEditorWidget

from webapp.models import Catalogo

class CatalogoForm(forms.ModelForm):

    class Meta:
        model = Catalogo
        fields = ['titulo', 'autor', 'fecha_inicial', 'fecha_final', 'descripcion', 'creditos', \
                  'informacion', 'actividades', 'categorias', 'website', 'portada']

        success_url = '/admin'

    def __init__(self, *args, **kwargs):
        super(CatalogoForm, self).__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs = {'placeholder': ''}
        self.fields['autor'].widget.attrs = {'placeholder': ''}
        self.fields['fecha_inicial'].widget = DateTimeWidget(usel10n=True, bootstrap_version=3)
        self.fields['fecha_final'].widget = DateTimeWidget(usel10n=True, bootstrap_version=3)
        self.fields['descripcion'].widget.attrs = {'placeholder': 'Descripciónn corta de la exposición...', 'rows': 3}
        self.fields['creditos'].widget = CKEditorWidget()
        self.fields['creditos'].initial = '<h2>Curaduría</h2><ul><li></li></ul>'
        self.fields['informacion'].widget = CKEditorWidget()
        self.fields['informacion'].initial = '<h2>Horarios</h2><ul><li></li><li></li></ul><hr><h2>Precios</h2><ul><li></li><li></li></ul>'
        self.fields['actividades'].widget = CKEditorWidget()
        self.fields['actividades'].initial = '<h2>Actividades</h2><ul><li></li><li></li></ul><hr><h2>Talleres</h2><ul><li></li><li></li></ul>'
        self.fields['website'].widget.attrs = {'placeholder': ''}
