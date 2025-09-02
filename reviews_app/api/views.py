from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated, AllowAny
from .filters import ReviewFilter
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissons import IsCreator, IsCustomer

class ReviewsView(generics.ListCreateAPIView):
    """
    A view for listing and creating reviews.

    - Supports GET requests to list all reviews with optional filtering and ordering.
    - Supports POST requests to create a new review for a business user by an authenticated customer.

    Attributes:
        queryset (QuerySet): The set of all reviews to be listed.
        serializer_class (ReviewSerializer): The serializer used for serializing review data.
        pagination_class (None): Disables pagination for the review list.
        filter_backends (list): The filters applied to the reviews, including DjangoFilterBackend for filtering and OrderingFilter for ordering.
        filterset_class (ReviewFilter): The filter set class that defines how reviews can be filtered.
        ordering_fields (list): The fields available for ordering the reviews (rating and updated_at).
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'updated_at']

    def perform_create(self, serializer):
        """
        Custom logic to prevent a user from writing multiple reviews for the same business user.
        
        Args:
            serializer: The serializer instance that is saving the review.

        Raises:
            PermissionDenied: If the reviewer has already written a review for the same business user.
        """
        reviewer = self.request.user
        business_user = serializer.validated_data.get('business_user')
        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise PermissionDenied(detail='You have already written a review for this business user.')
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the HTTP method:
        - `GET` allows any authenticated user to view the reviews.
        - `POST` only allows customers to create reviews.
        
        Returns:
            list: The list of permissions for the view.
        """
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsCustomer]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a specific review.
    
    - Supports GET to retrieve a specific review.
    - Supports PUT/PATCH to update an existing review.
    - Supports DELETE to remove a review.

    Attributes:
        queryset (QuerySet): The set of all reviews, used for retrieving, updating, or deleting.
        serializer_class (ReviewUpdateSerializer): The serializer used for updating review data.
        permission_classes (list): The permissions required for interacting with the review (only the creator can modify it).
    """
    queryset = Review.objects.filter()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsCreator]
