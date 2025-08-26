from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissons import IsBusinessUser
from offers_app.models import Offer
from offers_app.api.serializers import OfferGetSerializer, OfferPostSerizalizer

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferPostSerizalizer
        return OfferGetSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsBusinessUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

