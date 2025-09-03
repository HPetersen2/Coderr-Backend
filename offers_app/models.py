from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

OFFER_CHOICES = [
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium")
]

class Offer(models.Model):
    """
    Represents an offer created by a user.
    Fields:
        user: ForeignKey to User, linking the offer to its creator.
        title: Title of the offer (max 50 chars).
        image: Optional image uploaded to 'media/'.
        description: Brief description (max 255 chars).
        created_at: Timestamp when created (auto-set).
        updated_at: Timestamp when updated (auto-set).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="media/", blank=True, null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        short_desc = (self.description[:50] + '...') if len(self.description) > 50 else self.description
        return f"{self.title} by {self.user} – {short_desc}"


class OfferDetail(models.Model):
    """
    Contains detailed information for an Offer.
    Fields:
        offer: ForeignKey to Offer, allowing multiple details per offer.
        title: Title of the detail.
        revisions: Number of revisions allowed (positive integer).
        delivery_time_in_days: Delivery time in days (positive integer).
        price: Price (up to 10 digits, 2 decimals).
        features: List of features (JSONField).
        offer_type: Type of offer ('basic', 'standard', 'premium').
    """
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=25, choices=OFFER_CHOICES)
    
    def __str__(self):
        return f"{self.title} ({self.offer_type}) for {self.offer.title} – ${self.price}"

