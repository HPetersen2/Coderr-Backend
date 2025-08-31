from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg

from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import UserProfile

class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = {
            "review_count": Review.objects.count(),
            "average_rating": round(Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0, 1),
            "business_profile_count": UserProfile.objects.filter(type="business").count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
    
