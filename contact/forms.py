from django import forms
from .models import Enquiry


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'name': 'name',
    }))
    email = forms.CharField(min_length=11, required=True,  widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'name': 'email',
    }))
    subject = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'subject',
        'name': 'subject',
    }))
    message = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={
        'rows': 2,
        'class': 'form-control md-textarea',
        'id': 'message',
        'name': 'message',
    }))

