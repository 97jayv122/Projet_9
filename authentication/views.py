"""
Views for user authentication and profile management.

This module provides views for user signup, profile photo upload,
and password change functionalities.

Functions:
    signup(request):
        Display and process the user registration form. On GET,
        renders an empty signup form.
        On POST, validates and creates a new user, logs them in,
        and redirects to LOGIN_REDIRECT_URL.

    upload_profile_photo(request):
        Display and handle the profile photo upload
        form for the logged-in user.
        On GET, shows the form pre-populated with the current user.
        On POST, validates and saves the new profile photo,
        then redirects to the home page.

    password_change(request):
        Display and process the password change form for the logged-in user.
        On GET, renders the password change form with Bootstrap styling.
        On POST, validates and updates the user's password,
        then redirects to the password_change_done page.

"""
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
    """"""
Authentication views for the LITRevu application.

Provides:
- User signup (registration) and immediate login.
- Profile photo upload for authenticated users.
- Password change flow with session preservation to avoid logout.

Each view handles both GET (display form) and
POST (validate & process) requests,and redirects appropriately on success.
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

    On GET: show the UploadProfilePhotoForm pre-populated
    with the current user.
    On POST: bind POST + FILES to that form, validate,
    save the new image,
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
    return render(request, 'authentication/registration.html',
                  context={'form': form})
