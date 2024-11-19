# text_corrector/forms.py
from django import forms
from django.forms import ModelForm
from .models import *
from .models import Forum
from .models import Pregunta
from django.db import models
from .models import Diccionario


class TextInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Texto a corregir')

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'contenido']

class CreateInForum(ModelForm):
    class Meta:
        model= Forum
        fields = "__all__"

class CreateInDiscussion(ModelForm):
    class Meta:
        model= Discussion
        fields = "__all__"

class DiccionarioForm(forms.ModelForm):
    class Meta:
        model = Diccionario
        fields = '__all__'  # O lista de campos específicos que quieres en el formulario

