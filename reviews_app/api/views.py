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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'updated_at']

    def perform_create(self, serializer):
        reviewer = self.request.user
        business_user = serializer.validated_data.get('business_user')
        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise PermissionDenied(detail='You have already written a review for this business user.')
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsCustomer]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.filter()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsCreator]
