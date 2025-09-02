from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg

from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import UserProfile

class BaseInfoView(APIView):
    """
    A view that provides basic statistics about the system.
    
    - Returns the total number of reviews, average rating, count of business profiles,
    and the total number of offers in the system.

    Attributes:
        permission_classes (list): Specifies that the view is accessible to any user, regardless of authentication.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to retrieve basic system statistics.

        - `review_count`: The total number of reviews in the system.
        - `average_rating`: The average rating of all reviews, rounded to one decimal place.
        - `business_profile_count`: The total number of business user profiles.
        - `offer_count`: The total number of offers in the system.

        Args:
            request: The incoming HTTP request.
            *args, **kwargs: Additional arguments that may be passed (not used in this method).

        Returns:
            Response: A response containing the requested data in a dictionary format.
        """
        data = {
            "review_count": Review.objects.count(),  # Total number of reviews
            "average_rating": round(Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0, 1),  # Average rating rounded to one decimal
            "business_profile_count": UserProfile.objects.filter(type="business").count(),  # Total number of business profiles
            "offer_count": Offer.objects.count(),  # Total number of offers
        }
        return Response(data)
