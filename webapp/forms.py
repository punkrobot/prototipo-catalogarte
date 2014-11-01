# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from datetimewidget.widgets import DateTimeWidget
from ckeditor.widgets import CKEditorWidget

from webapp.models import Exposicion, Museo

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


class MuseoForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Contraseña')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Repetir contraseña')
    email = forms.EmailField(required=False, label='Correo electrónico')

    class Meta:
        model = Museo
        fields = ['username', 'password1', 'password2', 'email', 'nombre', 'direccion', 'detalles', \
            'website', 'twitter', 'facebook', 'instagram', 'youtube', 'logotipo', 'portada']

    def __init__(self, *args, **kwargs):
        super(MuseoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'placeholder': ''}

        self.fields['username'].widget.attrs = {'placeholder': 'Nombre de usuario'}
        self.fields['detalles'].widget = CKEditorWidget()
        self.fields['detalles'].initial = '<h3>Horarios</h3><ul><li></li></ul>'
        self.fields['website'].widget.attrs = {'placeholder': 'Sitio web oficial del museo'}

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise forms.ValidationError("El nombre de usuario ya existe.")


    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        return self.cleaned_data

    def save(self):
        usuario = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password1'])
        self.instance.user = usuario
        self.instance.save()
        return self.instance
