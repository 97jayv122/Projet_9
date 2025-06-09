from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  ['follows']

class TicketForm(forms.ModelForm):

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        
        
class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
