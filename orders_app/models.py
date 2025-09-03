from django.db import models
from django.contrib.auth import get_user_model
from offers_app.models import OfferDetail

User = get_user_model()

STATUS_CHOICES = [
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

class Order(models.Model):
    """
    A model representing an order in the system. This model holds information about 
    the order's status, price, associated users (customer and business), and the related offer details.

    Attributes:
        customer_user (ForeignKey): The user who placed the order (customer).
        business_user (ForeignKey): The user representing the business that handles the order.
        offer_detail (ForeignKey): The specific offer related to the order.
        price (DecimalField): The price of the order.
        status (CharField): The status of the order, selected from predefined choices (in_progress, completed, cancelled).
        created_at (DateTimeField): The timestamp when the order was created.
        updated_at (DateTimeField): The timestamp when the order was last updated.
    """
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.PROTECT, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id}: {self.customer_user} → {self.business_user} | {self.offer_detail} | {self.status} | ${self.price}"
