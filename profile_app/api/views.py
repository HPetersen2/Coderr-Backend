from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Profile
from .serializers import ProfileDetailSerializer
from .permissons import IsOwner

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.filter()
    serializer_class = ProfileDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()
    
class ProfileBusinessList(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
