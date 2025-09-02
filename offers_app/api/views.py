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
    This view handles the listing of all offers and creation of new offers.
    
    Attributes:
        queryset: A QuerySet that retrieves all offers from the database.
        pagination_class: Defines the pagination behavior for listing offers (limit per page).
        filter_backends: A list of filter backends used to filter, search, and order the offer data.
        filterset_class: Defines the filterset to apply filtering to the offer data.
        search_fields: A list of fields to enable search functionality.
        ordering_fields: A list of fields to enable ordering functionality.
    """
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_queryset(self):
        """
        Customize the queryset for listing offers.
        
        - Selects the related 'user' field to reduce the number of queries.
        - Prefetches the 'details' related model to optimize database access.
        - Annotates the offers with the minimum price and minimum delivery time
          from the related 'details' model.
        
        Returns:
            QuerySet: The optimized and annotated queryset for listing offers.
        """
        return (
            super().get_queryset()
            .select_related('user')  # Optimizing user-related queries
            .prefetch_related('details')  # Prefetch related offer details to reduce query count
            .annotate(
                min_price=Min('details__price'),  # Annotates with the minimum price from offer details
                min_delivery_time=Min('details__delivery_time_in_days'),  # Annotates with the minimum delivery time
            )
        )

    def perform_create(self, serializer):
        """
        Override the default create behavior to associate the offer with the current user.

        Args:
            serializer (OfferPostSerializer): The serializer used to create the offer.
        """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the HTTP method.
        
        - POST: Uses the OfferPostSerializer for offer creation.
        - GET: Uses the OfferGetSerializer for listing offers.

        Returns:
            class: The serializer class for the given HTTP method.
        """
        if self.request.method == 'POST':
            return OfferPostSerializer
        return OfferGetSerializer
    
    def get_permissions(self):
        """
        Assign appropriate permissions based on the HTTP method.

        - GET: No special permissions, available to all users.
        - POST: Restrict to business users only, as creating offers is a business-specific action.

        Returns:
            list: A list of permission classes for the request method.
        """
        if self.request.method == 'GET':
            permission_classes = []  # No special permissions for GET requests
        elif self.request.method == 'POST':
            permission_classes = [IsBusinessUser]  # Restrict POST to business users
        return [permission() for permission in permission_classes]
    

class OfferView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles the retrieval, update, and deletion of a specific offer.
    
    Attributes:
        queryset (QuerySet): A QuerySet to retrieve offers.
        serializer_class (Serializer): The serializer used to serialize the offer data.
    """
    queryset = Offer.objects.all()  # Base queryset for the view

    def get_queryset(self):
        """
        Customize the queryset for retrieving, updating, or deleting an offer.
        
        - Uses select_related to optimize queries for the related 'user'.
        - Uses prefetch_related to optimize queries for related 'details'.
        - Annotates each offer with the minimum price and minimum delivery time
          from its related details.

        Returns:
            QuerySet: The optimized and annotated queryset for the offer.
        """
        return (
            super().get_queryset()
            .select_related('user')  # Optimizes foreign key lookup for the user field
            .prefetch_related('details')  # Prefetches related offer details for efficiency
            .annotate(
                min_price=Min('details__price'),  # Adds min_price field to each offer
                min_delivery_time=Min('details__delivery_time_in_days'),  # Adds min_delivery_time field to each offer
            )
        )
    
    def get_permissions(self):
        """
        Assign appropriate permissions based on the HTTP method.
        
        Rules:
        - GET: User must be authenticated.
        - PATCH: User must be authenticated and the owner of the offer.
        - DELETE: User must be authenticated and the owner of the offer.

        Returns:
            list: A list of instantiated permission classes for the request method.
        """
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]  # Any authenticated user can view offers
        elif self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsOwner]  # Only the owner can update
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsOwner]  # Only the owner can delete
        else:
            permission_classes = [IsAuthenticated]  # Default case
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Choose the serializer class dynamically based on the HTTP method.
        
        - GET: Uses OfferDetailGetSerializer for detailed read-only representation.
        - PATCH: Uses OfferSerializer for updates.
        - DELETE: Defaults to OfferSerializer (serializer not really used here, but required).

        Returns:
            Serializer: The serializer class to be used for the current request.
        """
        if self.request.method == 'GET':
            return OfferDetailGetSerializer
        elif self.request.method == 'PATCH':
            return OfferSerializer
        return OfferSerializer  # Default fallback for DELETE or other methods
    


class OfferDetailView(generics.RetrieveAPIView):
    """
    This view handles retrieving detailed information about a specific offer detail.
    
    Attributes:
        queryset: A QuerySet to retrieve offer details.
        permission_classes: Restricts access to authenticated users.
        serializer_class: The serializer used to serialize the offer detail data.
    """
    queryset = OfferDetail.objects.all()
    permission_classes = [IsAuthenticated]  # Only authenticated users can view offer details
    serializer_class = OfferDetailSerializer
