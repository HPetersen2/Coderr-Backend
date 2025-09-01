from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from offers_app.models import Offer, OfferDetail


class OfferDetailGetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offer-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = Offer
        fields = ['id', 'url']

class OfferUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']


class OfferGetSerializer(serializers.ModelSerializer):
    details = OfferDetailGetSerializer(many=True)
    user_details = OfferUserSerializer(source='user')
    min_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        extra_kwargs = {
            'offer': {'read_only': True},
            'user': {'read_only': True}
        }

class OfferPostSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Ein Offer muss mindestens 3 Details enthalten.')
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance = super().update(instance, validated_data)

        if details_data is not None:
            if len(details_data) < 3:
                raise serializers.ValidationError('Ein Offer muss mindestens 3 Details enthalten.')

            for detail_data in details_data:
                detail_id = detail_data.get('id')

                if detail_id:
                    try:
                        offer_detail = instance.details.get(id=detail_id)
                        for attr, value in detail_data.items():
                            setattr(offer_detail, attr, value)
                        offer_detail.save()
                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError(f"OfferDetail mit ID {detail_id} existiert nicht.")
                else:
                    OfferDetail.objects.create(offer=instance, **detail_data)
    
class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailGetSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
    