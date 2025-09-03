from rest_framework import serializers
from reviews_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model, used for serializing and deserializing review data.
    This serializer is primarily used for displaying the full review details, including
    business user, reviewer, rating, description, and timestamps.

    Meta:
        model (Review): The model this serializer is based on.
        fields (list): The list of fields to include in the serialized representation.
        read_only_fields (list): Fields that are read-only and cannot be modified.
    """
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the review data, particularly for the rating and description fields.
    This serializer is used when a user wants to update an existing review.

    Meta:
        model (Review): The model this serializer is based on.
        fields (list): The list of fields that can be updated (rating and description).
    """
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
