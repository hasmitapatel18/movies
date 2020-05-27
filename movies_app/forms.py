from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields=['film_title', 'year', 'genre', 'summary']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',  )

PhotoFormSet=inlineformset_factory(Film, Photo, fields=( 'image',), extra=1, max_num=1, can_delete = False)
