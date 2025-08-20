from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from ..models import Profile
from .serializers import ProfileDetailSerializer, ProfileTypeSerializer
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


class ProfileBusinessList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__userprofile__type__iexact='business')


class ProfileCustomerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__userprofile__type__iexact='customer')
