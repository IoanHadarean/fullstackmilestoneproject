from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    """Render the registration page"""
    form = UserCreationForm()
    args = {'form': form }
    return render(request, 'register.html', args)
