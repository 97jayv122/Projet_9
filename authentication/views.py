from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms

def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'authentication/signup.html', context={'form': form})

def upload_profile_photo(request):
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