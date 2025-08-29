from django.db.models import Min
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissons import IsBusinessUser, IsOwner
from .pagination import OfferPagination
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferGetSerializer, OfferPostSerializer, OfferDetailSerializer

class OfferListView(generics.ListCreateAPIView):
    pagination_class = OfferPagination

    def get_queryset(self):
        return (
            Offer.objects.all()
            .select_related('user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferPostSerializer
        return OfferGetSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        elif self.request.method == 'POST':
            permission_classes = [IsBusinessUser]
        return [permission() for permission in permission_classes]
    
class OfferView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.filter()
    permission_classes = [IsAuthenticated, IsOwner]
    
class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer

