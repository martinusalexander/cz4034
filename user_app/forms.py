from django import forms
from models import *

class SearchDocumentsForm(forms.Form):
    search_keyword = forms.CharField(label='Keyword',
                                     max_length=500,
                                     widget=forms.TextInput(
                                         attrs={
                                             'placeholder': 'Enter the search keyword',
                                         }
                                     ))