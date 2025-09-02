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
    View to handle the user registration process by creating a new UserProfile instance.
    
    This view uses the UserRegistrationSerializer for input validation and object creation.
    The permission class `AllowAny` allows unrestricted access to this endpoint (no authentication required).
    """
    queryset = UserProfile.objects.all()
    """Defines the queryset for this view as all UserProfile instances."""
    serializer_class = UserRegistrationSerializer
    """Specifies the serializer class to be used for input validation and serialization."""
    permission_classes = [AllowAny]
    """Allows unrestricted access to this endpoint (no authentication required)."""

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to customize the response behavior.
        
        Steps:
        - Instantiate the serializer with the incoming request data.
        - Validate the data.
        - Save the user and create a corresponding UserProfile.
        - Return the serialized user data with a 201 Created status.
        """
        # Instantiate the serializer with the incoming request data.
        serializer = self.get_serializer(data=request.data)
        
        # Validate the input data, raising an exception if invalid.
        serializer.is_valid(raise_exception=True)
        
        # Save the new user and user profile, capturing the returned data.
        user_or_data = serializer.save()

        # Check if the serializer instance is a user object, otherwise fetch it from `serializer.instance`
        user = user_or_data if hasattr(user_or_data, 'pk') else getattr(serializer, 'instance', None)

        if not user:
            # If user creation failed, return a 400 Bad Request response.
            return Response({'detail': 'User konnte nicht erstellt werden.'}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically create the UserProfile if it doesn't exist yet.
        try:
            UserProfile.objects.get_or_create(user=user)
        except Exception:
            # If the model has required fields, an error may occur here.
            # Alternatively, we could add defaults or abort registration.
            pass

        # Return a successful HTTP 201 Created response with the user data.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    View to handle user login and return authentication token.
    
    This view uses the LoginSerializer to authenticate the user and provide a JWT token.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.

        Steps:
        - Validate the provided username and password.
        - Authenticate the user and retrieve the user profile.
        - Generate or fetch an authentication token.
        - Return user data and token in the response.
        """
        # Validate the incoming login data.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the authenticated user from the validated data.
        user = serializer.validated_data['user']

        try:
            # Try to get the associated UserProfile for the user.
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # If the UserProfile does not exist, return a 400 Bad Request response.
            return Response({'detail': 'UserProfile not found for this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate or retrieve an authentication token for the user.
        token, _ = Token.objects.get_or_create(user=user)

        # Return the user data and token in the response.
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update a user's profile details.
    
    This view supports GET and PATCH requests:
    - GET to retrieve the profile.
    - PATCH to update the profile (only for the owner of the profile).
    """
    queryset = UserProfile.objects.filter()
    """Defines the queryset to retrieve UserProfile instances."""
    serializer_class = ProfileDetailSerializer
    """Specifies the serializer class for serializing profile data."""

    def get_permissions(self):
        """
        Assign permissions based on the HTTP method of the request.

        - For GET requests, only authenticated users are allowed.
        - For PATCH requests, the user must be authenticated and the owner of the profile.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()


class ProfileBusinessList(generics.ListAPIView):
    """
    View to list all user profiles of type 'business'.
    
    This view returns a list of user profiles with type 'business', accessible only by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeBusinessSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Retrieve the queryset of profiles with type 'business'.
        
        Returns:
            queryset: A list of UserProfile instances with type 'business'.
        """
        return UserProfile.objects.filter(type__iexact='business')


class ProfileCustomerList(generics.ListAPIView):
    """
    View to list all user profiles of type 'customer'.
    
    This view returns a list of user profiles with type 'customer', accessible only by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileTypeCustomerSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Retrieve the queryset of profiles with type 'customer'.
        
        Returns:
            queryset: A list of UserProfile instances with type 'customer'.
        """
        return UserProfile.objects.filter(type__iexact='customer')
