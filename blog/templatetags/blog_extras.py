"""
docstring: Custom template tags and filters for the blog application.
Provides:
- model_type: Returns the model name of an instance.
- get_poster_display: Displays 'you' for the current user or their username.
- get_posted_at_display: Formats the time since a post was created.
- get_updated_at_display: Formats the time since a post was updated.
- is_reviewed_by: Checks if a user has reviewed a ticket.
- is_author: Checks if a user is the author of an instance.
- to_int: Converts a value to an integer, returning 0 on failure.
"""
from datetime import timedelta
from django.template import Library
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = Library()

@register.filter
def model_type(value):
    """
    Return the model name of the given instance (e.g., 'ticket', 'review').
    """
    return type(value).__name__

@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    """
    Return 'you' if the given user is the current request user; otherwise, return their username.
    """
    if user == context['user']:
        return 'vous avez'
    return user.username + ' a'

@register.simple_tag
def get_posted_at_display(posted_at):
    """
    Return a human-readable string indicating how long ago the post was created.
    """
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'il y a {int(seconds_ago // MINUTE)} minutes'
    if seconds_ago <= DAY:
        return f'il y a {int(seconds_ago // HOUR)} heures.'
    return f'le {posted_at.strftime("%d %b %Y à %Hh%M")}'

@register.simple_tag
def get_updated_at_display(created_at, updated_at):
    """
    Return a human-readable string for the update time if it is later than creation;
    otherwise return an empty string.
    """
    if not updated_at:
        return ''
    if updated_at - created_at < timedelta(seconds=1):
        return ''
    seconds_ago = (timezone.now() - updated_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Modifié il y a {int(seconds_ago // MINUTE)} minutes'
    if seconds_ago <= DAY:
        return f'Modifié il y a {int(seconds_ago // HOUR)} heures'
    return f'Modifié le {updated_at.strftime("%d %b %Y à %Hh%M")}'

@register.filter
def is_reviewed_by(ticket, user):
    """
    Return True if the given user has already posted a review for this ticket.
    """
    return ticket.review_set.filter(user=user).exists()

@register.filter
def is_author(instance, user):
    """
    Return True if the given user is the author of the instance.
    """
    return instance.user == user

@register.filter
def to_int(value):
    """
    Attempt to convert the given value to an integer; return 0 on failure.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
