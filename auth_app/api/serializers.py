from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer für die Benutzerregistrierung mit Validierung und Erstellung von User und UserProfile.
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
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Email oder Benutzername bereits vergeben.")
        return data

    def create(self, validated_data):
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
        token, _ = Token.objects.get_or_create(user=instance)
        return {
            'token': token.key,
            'username': instance.username,
            'email': instance.email,
            'user_id': instance.id,
        }

class LoginSerializer(serializers.Serializer):
    """
    Serializer für den Login mit Validierung der Anmeldedaten (Benutzername, Passwort).
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültiger Benutzername oder Passwort.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Ungültiger Benutzername oder Passwort.")

        data['user'] = user
        return data

class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer für das Abrufen und Bearbeiten von Benutzerprofilen.
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
    Serializer für Business-Benutzerprofile.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

class ProfileTypeCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer für Customer-Benutzerprofile.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']