from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Extends Django's User model with additional profile information.

    Fields:
        user: One-to-one link to Django User (cascade delete).
        type: User type, 'customer' or 'business'.
        first_name: Optional first name.
        last_name: Optional last name.
        file: Optional profile image uploaded to 'uploads/'.
        uploaded_at: Timestamp of last file upload.
        location: Required user location (city/region).
        tel: Optional telephone number.
        description: Required description of the user/business.
        working_hours: Optional working hours.
        created_at: Timestamp when profile was created.
    """
    
    UserType_CHOICES = [
        ('customer', 'Customer-User'),
        ('business', 'Business-User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=20, choices=UserType_CHOICES)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        display_name = full_name if full_name else self.user.username
        return f"{display_name} ({self.get_type_display()}) – {self.location}"
