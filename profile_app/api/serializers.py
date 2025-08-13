from rest_framework import serializers
from ..models import Profile

class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    first_name = serializers.PrimaryKeyRelatedField(source='user.firstname', read_only=True)
    last_name = serializers.PrimaryKeyRelatedField(source='user.lastname', read_only=True)
    type = serializers.PrimaryKeyRelatedField(source='profile.type', read_only=True)
    email = serializers.PrimaryKeyRelatedField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']