from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Model representing additional user profile information linked to the built-in Django User.

    This model extends the default Django User model with additional attributes such as the user's
    first name, last name, file upload, location, telephone number, description, and working hours.
    The 'type' attribute distinguishes between 'customer' and 'business' users.

    Attributes:
        user (OneToOneField): A one-to-one relationship to the Django User model.
            Ensures each UserProfile corresponds to exactly one User.
            Cascade deletion ensures that deleting the User deletes the UserProfile as well.
        type (CharField): Specifies the type of user.
            Choices are restricted to 'customer' or 'business'.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        file (ImageField): A profile image uploaded by the user.
        uploaded_at (DateTimeField): The date and time the file was uploaded.
        location (CharField): The user's location (e.g., city or region).
        tel (CharField): The user's phone number.
        description (TextField): A brief description of the user or business.
        working_hours (CharField): The user's or business's working hours.
        created_at (DateTimeField): The date and time the user profile was created.
    """

    UserType_CHOICES = [
        ('customer', 'Customer-User'),
        ('business', 'Business-User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """
    One-to-one relationship with the built-in User model.
    Ensures each UserProfile corresponds to exactly one User.
    If the User is deleted, the related UserProfile is also deleted (cascade deletion).
    """
    
    type = models.CharField(max_length=20, choices=UserType_CHOICES)
    """
    Specifies the type of user for the profile.
    The available choices are 'customer' and 'business'.
    This field helps distinguish between different user types.
    """
    
    first_name = models.CharField(max_length=100, blank=True)
    """
    The first name of the user.
    This field is optional (blank=True).
    """
    
    last_name = models.CharField(max_length=100, blank=True)
    """
    The last name of the user.
    This field is optional (blank=True).
    """
    
    file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    """
    Profile image for the user.
    The image is uploaded to the 'uploads/' directory.
    This field is optional and can be left blank or null.
    """
    
    uploaded_at = models.DateTimeField(auto_now=True)
    """
    Timestamp of when the file (profile image) was uploaded.
    This field is automatically set to the current date and time every time the instance is saved.
    """
    
    location = models.CharField(max_length=50)
    """
    The user's location (e.g., city or region).
    This field is required and cannot be left blank.
    """
    
    tel = models.CharField(max_length=20, blank=True)
    """
    The user's telephone number.
    This field is optional (blank=True).
    """
    
    description = models.TextField()
    """
    A text field where the user or business can describe themselves.
    This field is required and cannot be left blank.
    """
    
    working_hours = models.CharField(max_length=100, blank=True)
    """
    The working hours of the user or business.
    This field is optional and can be left blank.
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    """
    Timestamp of when the user profile was created.
    This field is automatically set to the current date and time when the instance is first created.
    """

    def __str__(self):
        """
        Returns a human-readable string representation of the UserProfile.

        The string representation includes the linked user's username and the user type (either 'customer' or 'business').
        This is useful when displaying the profile in Django admin or logs.
        """
        return f"{self.user.username} ({self.get_type_display()})"