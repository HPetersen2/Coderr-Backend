from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = [
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
]

OFFER_CHOICES = [
    ("basic", "basic")
]

class Order(models.Model):
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_oders")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=25, choices=OFFER_CHOICES)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="in-progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
