from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

OFFER_CHOICES = [
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium")
]

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="media/", blank=True, null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=25, choices=OFFER_CHOICES)