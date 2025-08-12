from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import UserProfile
from profile_app.models import Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Serializer for the UserProfile model used during user registration.
        Handles input fields for username, email, password, repeated password, and user type.
        """
        model = UserProfile
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """
        Perform custom validation on the incoming registration data.

        - Checks that the password and repeated password match.
        - Ensures the email and username are unique in the User model.

        Args:
            data (dict): The input data to validate.

        Raises:
            serializers.ValidationError: If passwords do not match or if
                                         username/email are already taken.

        Returns:
            dict: The validated data if all checks pass.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Email or username is already in use.")

        return data

    def create(self, validated_data):
        """
        Create a new User and corresponding UserProfile from the validated data.

        Steps:
        - Extract and remove email, username, password, and repeated_password from validated_data.
        - Create a new Django User instance with the given username, email, and password.
        - Create a UserProfile linked to the new User with remaining validated fields.
        - Generate or get an authentication token for the new User.
        - Return a dictionary containing the token and user info.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            dict: A dictionary including the auth token and user details.
        """
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user, **validated_data)
        Profile.objects.create(user=user)

        token, _ = Token.objects.get_or_create(user=user)

        return {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
            'type': profile.type,
        }
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login credentials.

    Defines the required input fields:
    - username: The username of the user attempting to log in.
    - password: The corresponding password for authentication.
    Both fields are write-only to avoid exposing sensitive information.
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the incoming login data.

        Steps:
        - Extract username and password from input data.
        - Attempt to retrieve a User object matching the username.
          Raises a validation error if no such user exists.
        - Use Django's authenticate function to verify the password.
          Raises a validation error if authentication fails.
        - Attach the authenticated User instance to the validated data
          for use in the view or further processing.

        Args:
            data (dict): The input login data containing username and password.

        Raises:
            serializers.ValidationError: If username does not exist or
                                         password authentication fails.

        Returns:
            dict: The validated data including the authenticated user instance.
        """
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data