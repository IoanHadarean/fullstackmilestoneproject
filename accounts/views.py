from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('login'))


def login(request):
    """
    Return the login page if the login form is valid
    else return an error message. Redirect the user back
    to the previous page for an url that requires login using
    next.
    """
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")

                if request.GET and request.GET['next'] != '':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('profile'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()

    args = {'login_form': login_form, 'next': request.GET.get('next', '')}
    return render(request, 'accounts/login.html', args)


def registration(request):
    """
    Render the registration page if the registration form
    is valid else return an error message.
    """
    if request.user.is_authenticated:
        return redirect(reverse('profile'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered! We have sent you a confirmation email!")
                """Send registration confirmation email"""
                send_mail(
                    'Wedding planner',
                    """
                    Thank you for registering to our website!
                    Feel free to explore our range of products!
                    Your username is : {}""".format(request.user.username),
                    'weddingplanner@email.com',
                    [request.user.email],
                    fail_silently=False,
                    )
                return redirect(reverse('profile'))
    else:
        registration_form = UserRegistrationForm()

    args = {'registration_form': registration_form}
    return render(request, 'accounts/registration.html', args)


@login_required
def profile(request):
    """
    Return the user's profile page. Allows editing the profile
    for a user.
    """

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, initial={'username': ''}, instance=request.user)
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
    return render(request, 'accounts/profile.html', context)
