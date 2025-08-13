from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Profile
from .serializers import ProfileDetailSerializer

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.filter()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]
