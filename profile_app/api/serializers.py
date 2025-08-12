from rest_framework import serializers
from ..models import Profile

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'file', 'location', 'tel', 'description', 'working_hours', 'created_at']
        # fields = ['user', 'username', 'firstname', 'lastname', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']