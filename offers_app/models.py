from django.db import models

OFFER_CHOICES = [
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium")
]

class Offer(models.Model):
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="media/", blank=True, null=True)
    description = models.CharField(max_length=255)

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=25, choices=OFFER_CHOICES)