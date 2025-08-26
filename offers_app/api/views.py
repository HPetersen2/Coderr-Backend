from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissons import IsBusinessUser
from offers_app.models import Offer
from offers_app.api.serializers import OfferSerizalizer

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerizalizer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsBusinessUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

