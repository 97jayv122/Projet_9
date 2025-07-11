"""
docstring: blog/models.py
This module defines the data models for the blog application,
including Ticket and Review.
It includes:
- Ticket: Represents a user-created ticket with a title,
  description, optional image, and timestamps.
- Review: Represents a user's review of a Ticket,
  including a rating, headline, optional body, and timestamps.
Both models handle image resizing and validation for ratings.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image

# Create your models here.
class Ticket(models.Model):
    """
    Represents a user-created ticket containing a title, description,
    optional image, and timestamps for creation and last update.

    Methods:
        resize_image(): Resize the uploaded image to fit within IMAGE_MAX_SIZE.
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        """
        Resize the uploaded image to fit within IMAGE_MAX_SIZE,
        preserving aspect ratio.
        """
        if not self.image:
            return
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        Override save method to ensure image resizing after initial save.
        """
        super().save(*args, **kwargs)
        self.resize_image()

class Review(models.Model):
    """
    Represents a user's review of a Ticket, including a rating,
    headline, optional body, and timestamps for creation and update.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    RATING_CHOICES = [(i, f"{i} étoile{'s' if i>1 else ''}") for i in range(1, 6)]
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
