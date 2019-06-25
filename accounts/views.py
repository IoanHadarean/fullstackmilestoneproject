from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Render the registration page"""
    form = UserCreationForm()
    return render(request, 'register.html')
