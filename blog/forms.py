from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class FollowUsersForm(forms.ModelForm):
    """
    A form for following another user by their username.

    Fields:
        username (CharField): The username of the user to follow.

    Cleaning and saving:
        clean_username: Validates that the username exists and returns the User instance.
        save: Adds the specified user to the current user's follows.
    """
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
        """
        Validates that the provided username corresponds to an existing user.

        Returns:
            User: The user instance to follow.

        Raises:
            forms.ValidationError: If no user matches the given username.
        """
        username = self.cleaned_data['username']
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                "Aucun utilisateur avec ce nom d’utilisateur."
                )
        return user_to_follow

    def save(self, commit=True):
        """
        Adds the cleaned user to the current user's follow list and saves the instance.

        Args:
            commit (bool): Whether to save the current user instance.

        Returns:
            User: The current user instance with updated follows.
        """
        current_user = self.instance
        user_to_follow = self.cleaned_data['username']
        current_user.follows.add(user_to_follow)
        if commit:
            current_user.save()
        return current_user


class TicketForm(forms.ModelForm):
    """
    A form for creating or editing a ticket with title, description, and optional image.

    Fields:
        edit_ticket (BooleanField): Hidden flag to differentiate edit operations.
        title (CharField): Title of the ticket.
        description (Textarea): Detailed description of the ticket.
        image (ClearableFileInput): Optional image upload for the ticket.
    """
    edit_ticket = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
        )

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
    """
    A hidden form used to confirm deletion of a ticket.

    Fields:
        delete_ticket (BooleanField): Hidden flag indicating deletion.
    """
    delete_ticket = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
        )  


class ReviewForm(forms.ModelForm):
    """
    A form for creating or editing a review with headline, rating, and body.

    Fields:
        edit_review (BooleanField): Hidden flag to differentiate edit operations.
        headline (CharField): Title of the review.
        rating (ChoiceField): Star rating selection.
        body (Textarea): Detailed review content.
    """
    edit_review = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
        )
    
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
    """
    A hidden form used to confirm deletion of a review.

    Fields:
        delete_review (BooleanField): Hidden flag indicating deletion.
    """
    delete_review = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
        )


class UnfolloUsersFrorm(forms.Form):
    """
    A hidden form used to confirm unfollowing a user.

    Fields:
        unfollow_user (BooleanField): Hidden flag indicating unfollow action.
    """
    unfollow_user = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
        )
