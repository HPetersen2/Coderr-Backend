from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with validation and creation of User and UserProfile.
    """
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """Ensures that the provided data is valid by checking password match and uniqueness of email and username."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Email or username already taken.")
        return data

    def create(self, validated_data):
        """Creates a new User and associated UserProfile, and generates an authentication token."""
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')
        user_type = validated_data.pop('type')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, type=user_type)

        token, _ = Token.objects.get_or_create(user=user)

        return user

    def to_representation(self, instance):
        """Returns a serialized representation of the user including token, username, email, and user ID."""
        token, _ = Token.objects.get_or_create(user=instance)
        return {
            'token': token.key,
            'username': instance.username,
            'email': instance.email,
            'user_id': instance.id,
        }

class LoginSerializer(serializers.Serializer):
    """
    Serializer for login with validation of login credentials (username, password).
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
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

class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profiles.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance

class ProfileTypeBusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for business user profiles.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

class ProfileTypeCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer user profiles.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']
