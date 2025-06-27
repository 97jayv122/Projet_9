from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Nom d'utilisateur"}),
        label=""
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Mot de passe"}),
        label=""
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirmer mot de passe"}),
        label=""
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

class UploadProfilePhotoform(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo',)


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': "Nom d'utilisateur",
        }),
        label=""
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe",
        }),
        label=""
    )