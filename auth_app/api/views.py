from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from ..models import UserProfile
from .serializers import UserRegistrationSerializer, LoginSerializer, ProfileDetailSerializer, ProfileTypeBusinessSerializer, ProfileTypeCustomerSerializer


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
        user_or_data = serializer.save()

        # serializer.save() sollte das User-Objekt zurückgeben; falls nicht, prüfen wir serializer.instance
        user = user_or_data if hasattr(user_or_data, 'pk') else getattr(
            serializer, 'instance', None)

        if not user:
            return Response({'detail': 'User konnte nicht erstellt werden.'}, status=status.HTTP_400_BAD_REQUEST)

        # Automatisch UserProfile anlegen (wenn noch nicht vorhanden)
        try:
            UserProfile.objects.get_or_create(user=user)
        except Exception:
            # Falls das Model Pflichtfelder hat, kann hier ein Fehler auftreten.
            # Alternativ defaults hinzufügen oder Registrierung abbrechen.
            pass

        """Return a successful HTTP 201 Created response with the user data."""
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile not found for this user.'}, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = ProfileTypeBusinessSerializer
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(type__iexact='business')


class ProfileCustomerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeCustomerSerializer
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(type__iexact='customer')
