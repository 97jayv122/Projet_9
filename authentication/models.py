"""
This module defines a custom user model for a Django application,
extending Django's built-in AbstractUser to include additional fields
for user profile management.
It includes:
- A profile photo field for user avatars.
- Many-to-many relationships for following and blocking other users.
This allows users to manage their social interactions within the application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    to include a profile photo, follow relationships,
    and block relationships between users.

    Attributes:
        profile_photo (ImageField): Optional profile image for the user.
        follows (ManyToManyField): Users that this user is following.
        blocked (ManyToManyField): Users that this user has blocked.
    """
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
        related_name='followers'
    )
    blocked = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='blocked_by',
        blank=True,
        verbose_name='bloqué',
    )
