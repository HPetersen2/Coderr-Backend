from django.db import models
from auth_app.models import UserProfile

STATUS_CHOICES = [
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
]

class Order(models.Model):
    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="customer_oders")
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="business_orders")
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="in-progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
