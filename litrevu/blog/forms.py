from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    username = forms.CharField(label="Nom d’utilisateur à suivre")

    class Meta:
        model = User
        fields = []

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Aucun utilisateur avec ce nom d’utilisateur.")
        return user_to_follow

    def save(self, commit=True):
        current_user = self.instance
        user_to_follow = self.cleaned_data['username']
        current_user.follows.add(user_to_follow)
        if commit:
            current_user.save()
        return current_user


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
                    'image': forms.ClearableFileInput(attrs={'required': False}),
                    'description': forms.Textarea(attrs={
                        'rows': 7,
                        'placeholder': 'Description',
                    })
                }
        labels = {
            'title'      : "Titre du billet :",
            'description': "Texte / Description :",
            'image'      : "Illustration (facultatif) :"
        }


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)  


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre de la critique',
            'rating': 'Note',
            'body': 'Commentaire'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 7,
                'placeholder': 'Votre commentaire…',
            }),
        }

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UnfolloUsersFrorm(forms.Form):
    unfollow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
