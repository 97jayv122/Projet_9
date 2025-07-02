from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            "placeholder": "Nom d'utilisateur"}),
        label=""
    )

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
                    'title': forms.TextInput(attrs={
                        'class': 'form-control',
                    }),
                    'image': forms.ClearableFileInput(attrs={
                        'class': 'form-control',
                        'required': False
                        }),
                    'description': forms.Textarea(attrs={
                        'class': 'form-control',
                        'rows': 7,
                    })
                }
        labels = {
            'title'      : "Titre du billet :",
            'description': "Description :",
            'image'      : "Illustration (facultatif) :"
        }
        error_messages = {
            'title' : {
                'required': '',
            },
            'description': {
                'required': '',
            }
            },


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
            'headline':forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'rating': forms.RadioSelect(
                attrs={'class': 'star-rating'}),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
            }),
        }

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UnfolloUsersFrorm(forms.Form):
    unfollow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
