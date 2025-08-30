from rest_framework import generics
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer, ReviewUpdateSerializer
from .permissons import IsCreator, IsCustomer

class ReviewsView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            permission_classes = [IsCustomer]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.filter()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsCreator]

