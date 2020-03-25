from typing import Tuple

from django import forms
from .models import Post, Cevap
from pagedown.widgets import PagedownWidget

class SoruSorForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        labels = {
            'title': 'Başlık',
            'text': 'İçerik'
        }



class CevapForm(forms.ModelForm):
    class Meta:
        model = Cevap
        fields = ('icerik', )
        widgets = {
            'icerik': PagedownWidget()
        }


