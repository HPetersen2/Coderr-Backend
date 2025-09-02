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
    This model represents an offer made by a user. It includes basic information about the offer, such as its title, description, and associated user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    """
    A foreign key to the User model. This links the offer to the user who created it.
    The 'related_name' attribute specifies the reverse relationship from User to Offer.
    """
    title = models.CharField(max_length=50)
    """
    The title of the offer, with a maximum length of 50 characters.
    """
    image = models.FileField(upload_to="media/", blank=True, null=True)
    """
    An optional image file related to the offer. The file will be uploaded to the 'media/' directory.
    """
    description = models.CharField(max_length=255)
    """
    A brief description of the offer. It has a maximum length of 255 characters.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """
    Automatically sets the date and time when the offer is created.
    """
    updated_at = models.DateTimeField(auto_now=True)
    """
    Automatically updates the date and time whenever the offer is updated.
    """
    
    def __str__(self):
        """
        String representation of the offer. It will return the title of the offer.
        """
        return self.title

class OfferDetail(models.Model):
    """
    This model contains the detailed information about an individual offer, such as price, revisions, delivery time, and features.
    Each offer can have multiple details associated with it.
    """
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    """
    A foreign key to the Offer model. This establishes a one-to-many relationship, where an offer can have multiple details.
    'related_name' specifies the reverse relationship from Offer to OfferDetail.
    """
    title = models.CharField(max_length=50)
    """
    The title for the offer detail. This can describe specific revisions or aspects of the offer.
    """
    revisions = models.PositiveIntegerField()
    """
    The number of revisions allowed for the offer detail. This is a positive integer.
    """
    delivery_time_in_days = models.PositiveIntegerField()
    """
    The delivery time for this offer detail, expressed in days. This is a positive integer.
    """
    price = models.DecimalField(max_digits=10, decimal_places=2)
    """
    The price of the offer detail. It allows for a maximum of 10 digits, with up to 2 decimal places for precision.
    """
    features = models.JSONField(default=list)
    """
    A list of features related to this offer detail. This uses a JSON field to store an array of features.
    """
    offer_type = models.CharField(max_length=25, choices=OFFER_CHOICES)
    """
    The type of offer, which can be one of 'basic', 'standard', or 'premium'.
    The choices are defined in the OFFER_CHOICES list, ensuring only valid options can be selected.
    """
    
    def __str__(self):
        """
        String representation of the offer detail. Returns the title of the offer detail.
        """
        return self.title
