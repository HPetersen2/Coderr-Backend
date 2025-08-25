from rest_framework import serializers
from offers_app.models import Offer

class OfferSerizalizer(serializers.ModelSerializer):
    details = serializers.JSONField(source='detail')
    class Meta:
        model = Offer
        fields = '__all__'