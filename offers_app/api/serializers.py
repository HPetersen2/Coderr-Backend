from rest_framework import serializers
from offers_app.models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        extra_kwargs = {
            "offer": {"read_only": True}
        }

class OfferSerizalizer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Ein Offer muss mindestens 3 Details enthalten.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer