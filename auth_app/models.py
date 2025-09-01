from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Model representing additional user profile information linked to the built-in Django User.

    Attributes:
        user (OneToOneField): A one-to-one relationship to the Django User model.
            Ensures each UserProfile corresponds to exactly one User.
            Cascade deletion ensures that deleting the User deletes the UserProfile as well.
        type (CharField): Specifies the type of user.
            Choices are restricted to 'customer' or 'business'.
    """

    UserType_CHOICES = [
        ('customer', 'Customer-User'),
        ('business', 'Business-User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=UserType_CHOICES)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    location = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a human-readable string representation of the UserProfile,
        showing the linked user's username and the user type.
        """
        return f"{self.user.username} ({self.get_type_display()})"
    