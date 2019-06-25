from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Form to be used to log users in"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
