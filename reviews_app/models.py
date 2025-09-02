from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    """
    A model representing a review for a business user, created by a reviewer.
    This model holds information about the rating, description, and timestamps of the review.

    Attributes:
        business_user (ForeignKey): The user (business) being reviewed.
        reviewer (ForeignKey): The user who is writing the review.
        rating (PositiveIntegerField): The rating given to the business, between 1 and 5.
        description (CharField): A textual description or comment provided by the reviewer.
        created_at (DateTimeField): The timestamp when the review was created.
        updated_at (DateTimeField): The timestamp when the review was last updated.
    """
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_user')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
