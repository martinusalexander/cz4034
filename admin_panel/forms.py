from django import forms
from models.models import HOTEL_TYPE

class SignInForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=200,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'User Name'}))
    password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password'}))

class CreateUserForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=200,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'User Name'}))
    password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password'}))
    email = forms.CharField(label='Email', max_length=200,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='First Name', max_length=200,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Email', max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}))

class UpdateUserForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(label='User Name', max_length=200,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'User Name'}),
                               required=False)
    password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password'}),
                                required=False)
    email = forms.CharField(label='Email', max_length=200,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Email'}),
                                required=False)
    first_name = forms.CharField(label='First Name', max_length=200,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(label='Email', max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}),
                                required=False)

class ScrapeForm(forms.Form):
    search_keyword = forms.CharField(label='Keyword',
                                     max_length=500,
                                     widget=forms.TextInput(
                                         attrs={
                                             'placeholder': 'Enter the search keyword',
                                         }),
                                     required=True)

class UpdateLabelForm(forms.Form):
    id = forms.CharField(max_length=500,
                         widget=forms.HiddenInput(
                             attrs={}
                         ),
                         required=True)
    type = forms.ChoiceField(choices=HOTEL_TYPE,
                             widget=forms.Select(
                                 attrs={'onchange': 'change_label(this)'}),
                             required=True,
                             )