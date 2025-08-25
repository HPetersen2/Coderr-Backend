from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from offers_app.models import Offer
from offers_app.api.serializers import OfferSerizalizer

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerizalizer
    permission_classes = [IsAuthenticated]