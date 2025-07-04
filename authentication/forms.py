from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms


class SignupForm(UserCreationForm):
    """
    Form for registering a new user, extending Django's UserCreationForm.

    Fields:
        username: A unique username.
        password1: Password entry.
        password2: Password confirmation.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            "placeholder": "Nom d'utilisateur"}),
        label=""
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            "placeholder": "Mot de passe"
            }),
        label=""
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            "placeholder": "Confirmer mot de passe"
            }),
        label=""
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class UploadProfilePhotoform(forms.ModelForm):
    """
    Form for uploading or updating a user's profile photo.

    Fields:
        profile_photo: An image file for the user's avatar.
    """
    class Meta:
        model = get_user_model()
        fields = ('profile_photo',)
        widgets = {
            'profile_photo': forms.ClearableFileInput(
                attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with Bootstrap styling.

    Fields:
        username: The user's username, autofocus enabled.
        password: The user's password.
    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': True,
            'placeholder': "Nom d'utilisateur",
        }),
        label=""
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Mot de passe",
        }),
        label=""
    )