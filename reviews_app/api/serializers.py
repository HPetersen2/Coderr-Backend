from rest_framework import serializers
from reviews_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'description']

