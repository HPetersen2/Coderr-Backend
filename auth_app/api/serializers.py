from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Define an email field that is write-only (not returned in responses)."""
    email = serializers.EmailField(write_only=True)
    """Define password and repeated_password fields, both write-only to avoid exposing them."""
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """This serializer is based on the UserProfile model."""
        model = UserProfile
        """Specifies the fields that will be handled by this serializer."""
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """Custom validation method that runs before creating the user."""
        
        """Check if the password and repeated password match."""
        if data['password'] != data['repeated_password']:
            """Raise validation error if passwords do not match."""
            raise serializers.ValidationError("Passwords do not match.")
        
        """Check if a User with the given email already exists."""
        if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists():
            """Raise validation error if email or username is already taken."""
            raise serializers.ValidationError("Email or username is already in use.")
        
        """Return the validated data if all checks pass."""
        return data

    def create(self, validated_data):
        """Extract email and password from the validated data,
        and remove repeated_password as it is no longer needed."""
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        """Create a new User instance using the email as username."""
        user = User.objects.create_user(username=email, email=email, password=password)

        """Create the associated UserProfile instance with the remaining validated data."""
        profile = UserProfile.objects.create(user=user, **validated_data)

        """Generate or retrieve an authentication token for the new user."""
        token, _ = Token.objects.get_or_create(user=user)

        """Return a dictionary containing the token and some user info."""
        return {
            'token': token.key,
            'username': profile.username,
            'email': user.email,
            'user_id': user.id,
            'type': profile.type,
        }
    
class LoginSerializer(serializers.Serializer):
    """Define fields for username and password input."""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Extract the username and password from the incoming data."""
        username = data.get('username')
        password = data.get('password')

        """Attempt to retrieve the User object associated with the given username."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            """Raise validation error if user with this username does not exist."""
            raise serializers.ValidationError("Invalid username or password.")

        """Authenticate the user with the retrieved username and provided password."""
        user = authenticate(username=user.username, password=password)
        if not user:
            """Raise validation error if authentication fails."""
            raise serializers.ValidationError("Invalid username or password.")

        """Add the authenticated user to the validated data for further processing."""
        data['user'] = user
        return data