from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

def index(request):
    """Return the index.html file"""
    return render(request, 'index.html')
    
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('index'))
    
def login(request):
    """
    Return the login page if the login form is valid
    else return an error message. Redirect the user back
    to the previous page for an url that requires login using
    next.
    """
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
                                     
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('profile'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
            
    args = {'login_form': login_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', args)
        
def registration(request):
    """
    Render the registration page if the registration form
    is valid else return an error message.
    """
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
                                     
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered!")
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register your account at this time!')
                
    else:
        registration_form = UserRegistrationForm()
            
    args = {'registration_form': registration_form}
    return render(request, 'registration.html', args)
        
@login_required
def profile(request):
    """
    Return the user's profile page. Allows editing the profile
    for a user. 
    """
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, 
                                         request.FILES, 
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)