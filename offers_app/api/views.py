from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissons import IsBusinessUser
from .pagination import OfferPagination
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferGetSerializer, OfferPostSerizalizer, OfferDetailSerializer

class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
    
class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer

