from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissons import IsBusinessUser, IsOwner
from .pagination import OfferPagination
from .filters import OfferFilter
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferGetSerializer, OfferPostSerializer, OfferDetailSerializer, OfferSerializer, OfferDetailGetSerializer

class OfferListView(generics.ListCreateAPIView):
    """
    View for listing all offers and creating new ones.

    Attributes:
        queryset: Retrieves all offers.
        pagination_class: Sets pagination for offers.
        filter_backends: Specifies filters (search, ordering, etc.).
        filterset_class: Applies filtering to the offer data.
        search_fields: Allows searching on title and description.
        ordering_fields: Enables ordering by updated_at and min_price.
    """
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_queryset(self):
        """Optimizes and annotates offers with min price and delivery time."""
        return (
            super().get_queryset()
            .select_related('user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )

    def perform_create(self, serializer):
        """Associates the created offer with the current user."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Selects the serializer based on the HTTP method."""
        if self.request.method == 'POST':
            return OfferPostSerializer
        return OfferGetSerializer

    def get_permissions(self):
        """Assigns permissions based on the request method."""
        if self.request.method == 'GET':
            return []
        return [IsBusinessUser()]


class OfferView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific offer.

    Attributes:
        queryset: Retrieves all offers.
        serializer_class: The serializer for the offer data.
    """
    queryset = Offer.objects.all()

    def get_queryset(self):
        """Optimizes and annotates offers with related details."""
        return (
            super().get_queryset()
            .select_related('user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )
    
    def get_permissions(self):
        """Assigns permissions based on the HTTP method."""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Selects the serializer based on the HTTP method."""
        if self.request.method == 'GET':
            return OfferDetailGetSerializer
        return OfferSerializer


class OfferDetailView(generics.RetrieveAPIView):
    """
    View for retrieving detailed information about a specific offer detail.

    Attributes:
        queryset: Retrieves all offer details.
        permission_classes: Requires authentication.
        serializer_class: Serializes the offer detail data.
    """
    queryset = OfferDetail.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer

