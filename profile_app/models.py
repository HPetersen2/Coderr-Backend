from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    location = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"