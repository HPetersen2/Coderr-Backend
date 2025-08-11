from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    UserType_CHOICES = [
        ('customer', 'Customer-User'),
        ('business', 'Business-User')
    ]

    """
    This field creates a one-to-one relationship with the built-in Django User model.
    It ensures that each UserProfile is uniquely linked to one User instance.
    The 'on_delete=models.CASCADE' argument specifies that when the associated User is deleted,
    the UserProfile will be deleted as well, maintaining database integrity.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    """
    This field stores the full name of the user as a character string.
    The maximum length is limited to 255 characters to accommodate long names.
    """
    username = models.CharField(max_length=255)

    type = models.CharField(max_length=20, choices=UserType_CHOICES)
