from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from offers_app.models import Offer, OfferDetail

class OfferDetailGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer details in a read-only format, including a hyperlink to the offer details view.
    """
    url = serializers.HyperlinkedIdentityField(view_name='offer-detail', lookup_field='pk')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offer details, including title, revisions, delivery time, price, features, and offer type.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferUserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving basic user details (first name, last name, and username) associated with an offer.
    """
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']


class OfferGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer information along with associated details and user information.
    """
    details = OfferDetailGetSerializer(many=True)
    user_details = OfferUserSerializer(source='user')
    min_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offer details, including fields like title, revisions, price, and offer type.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        extra_kwargs = {
            'offer': {'read_only': True},
            'user': {'read_only': True}
        }


class OfferPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new offers, including validation for a minimum of three details per offer.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('An offer must have at least 3 details.')
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
        if details_data:
            if len(details_data) < 3:
                raise serializers.ValidationError('An offer must have at least 3 details.')
            for detail_data in details_data:
                detail_id = detail_data.get('id')
                if detail_id:
                    try:
                        offer_detail = instance.details.get(id=detail_id)
                        for attr, value in detail_data.items():
                            setattr(offer_detail, attr, value)
                        offer_detail.save()
                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError(f"OfferDetail with ID {detail_id} does not exist.")
                else:
                    OfferDetail.objects.create(offer=instance, **detail_data)
        return instance


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offers and their details, allowing partial updates.
    """
    details = OfferDetailPatchSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data.get("offer_type")
            try:
                detail = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"No detail found for offer_type '{offer_type}'"}
                )

            for attr, value in detail_data.items():
                if attr not in ["offer_type"]:
                    setattr(detail, attr, value)
            detail.save()

        return instance


class OfferDetailGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer details along with the associated offer's basic information.
    """
    details = OfferDetailGetSerializer(read_only=True, many=True)
    min_price = serializers.IntegerField()
    min_delivery_time = serializers.IntegerField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
