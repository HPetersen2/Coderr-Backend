from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from auth_app.models import UserProfile
from .serializers import UserRegistrationSerializer, LoginSerializer, ProfileDetailSerializer, ProfileTypeBusinessSerializer, ProfileTypeCustomerSerializer

class UserProfileCreateView(generics.CreateAPIView):
    """
    View to handle user registration by creating a new UserProfile instance.
    Uses `UserRegistrationSerializer` for input validation and object creation.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Validates the input data, creates the user and the UserProfile, and returns the user data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_or_data = serializer.save()
        user = user_or_data if hasattr(user_or_data, 'pk') else getattr(serializer, 'instance', None)

        if not user:
            return Response({'detail': 'User could not be created.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            UserProfile.objects.get_or_create(user=user)
        except Exception:
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    View for user login and providing an authentication token.
    Uses `LoginSerializer` for user authentication.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Validates the login credentials, authenticates the user, and returns a token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile not found.'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update a user's profile details.
    Supports GET for retrieval and PATCH for updates (only for profile owner).
    """
    queryset = UserProfile.objects.filter()
    serializer_class = ProfileDetailSerializer

    def get_permissions(self):
        """
        Assigns permissions based on the HTTP method:
        - GET: Only authenticated users.
        - PATCH: Authenticated users who are also the profile owner.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()


class ProfileBusinessList(generics.ListAPIView):
    """
    View to list all user profiles of type 'business'.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeBusinessSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Retrieves the list of 'business' type user profiles.
        """
        return UserProfile.objects.filter(type__iexact='business')


class ProfileCustomerList(generics.ListAPIView):
    """
    View to list all user profiles of type 'customer'.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeCustomerSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Retrieves the list of 'customer' type user profiles.
        """
        return UserProfile.objects.filter(type__iexact='customer')
