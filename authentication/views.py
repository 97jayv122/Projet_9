from django.conf import settings
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms


def signup(request):
    """
    Display and process the user registration form.

    On GET: instantiate an empty SignupForm and render the signup template.
    On POST: bind the submitted data, validate, create a new user,
    log them in, and redirect to LOGIN_REDIRECT_URL.
    """
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'authentication/signup.html', context={'form': form})

@login_required
def upload_profile_photo(request):
    """
    Display and handle the profile photo upload form for the logged-in user.

    On GET: show the UploadProfilePhotoForm pre-populated with the current user.
    On POST: bind POST + FILES to that form, validate, save the new image,
    and redirect back to the home page.
    """
    form = forms.UploadProfilePhotoform()
    if request.method == 'POST':
        form = forms.UploadProfilePhotoform(request.POST, request.FILES,
                                            instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,
                  'authentication/upload_photo_profile.html',
                  context={'form': form})

@login_required
def password_change(request):
    """
    Display and process the password change form for the logged-in user.

    On GET: instantiate PasswordChangeForm and apply Bootstrap styling.
    On POST: bind submitted data, validate, update the password,
    then redirect to the password_change_done page.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    return render(request, 'authentication/registration.html', context={'form': form})

