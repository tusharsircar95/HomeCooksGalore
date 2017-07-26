from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100)
    password = forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100)
    password = forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput)
    #email = forms.Char
