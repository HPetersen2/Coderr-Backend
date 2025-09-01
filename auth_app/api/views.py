from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissons import IsOwner
from ..models import UserProfile
from .serializers import UserRegistrationSerializer, LoginSerializer, ProfileDetailSerializer, ProfileTypeSerializer

class UserProfileCreateView(generics.CreateAPIView):
    """Defines the queryset for this view as all UserProfile instances."""
    queryset = UserProfile.objects.all()
    """Specifies the serializer class to be used for input validation and serialization."""
    serializer_class = UserRegistrationSerializer
    """Allows unrestricted access to this endpoint (no authentication required)."""
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Override the default create method to customize the response."""

        """Instantiate the serializer with the incoming request data."""
        serializer = self.get_serializer(data=request.data)
        """Validate the input data, raising an exception if invalid."""
        serializer.is_valid(raise_exception=True)
        """Save the new user and user profile, capturing the returned data."""
        data = serializer.save()
        """Return a successful HTTP 201 Created response with the user data."""
        return Response(data, status=status.HTTP_201_CREATED)
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        profile = UserProfile.objects.get(user=user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)
    

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.filter()
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
        return UserProfile.objects.filter(user__userprofile__type__iexact='business')


class ProfileCustomerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user__userprofile__type__iexact='customer')