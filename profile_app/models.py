from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='uploads/')
    location = models.CharField(max_length=50)
    tel = models.IntegerField()
    description = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=20)
