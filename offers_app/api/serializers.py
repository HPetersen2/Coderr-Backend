from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from offers_app.models import Offer, OfferDetail

class OfferDetailGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer details in a read-only format.

    This serializer is used when retrieving offer details. It includes a HyperlinkedIdentityField
    for the detailed view of the offer. The `url` field provides a hyperlink to the detailed view of an offer.

    Attributes:
        url (HyperlinkedIdentityField): A field to generate the URL for the offer details view.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='offer-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offer details.

    This serializer is used when updating the details of an offer. It includes fields such as
    the title, revisions, delivery time, price, features, and offer type, which are all editable
    during an update request.

    Attributes:
        title (str): The title of the offer detail.
        revisions (int): The number of revisions for the offer.
        delivery_time_in_days (int): The time required to deliver the offer in days.
        price (Decimal): The price of the offer.
        features (str): A description of the features of the offer.
        offer_type (str): The type of offer.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferUserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving basic user details associated with an offer.

    This serializer is used to return user details such as the first name, last name, and username of the user
    who created the offer.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        username (str): The user's username.
    """
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']


class OfferGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer information with associated details.

    This serializer is used to retrieve an offer, including its details, user details, minimum price, and minimum
    delivery time. The offer's basic attributes such as title, image, and description are also included.

    Attributes:
        details (OfferDetailGetSerializer): A nested serializer to retrieve offer details.
        user_details (OfferUserSerializer): A nested serializer to retrieve the details of the user who created the offer.
        min_price (Decimal): The minimum price of the offer.
        min_delivery_time (int): The minimum delivery time for the offer.
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
    Serializer for creating and updating offer details.

    This serializer is used when creating or updating offer details, including fields like title, revisions,
    delivery time, price, features, and offer type.

    Attributes:
        offer (Offer): The associated offer object (read-only).
        user (User): The user who created the offer (read-only).
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
    Serializer for creating new offers, including their details.

    This serializer is used when creating a new offer, and it requires the offer details to be provided
    as a nested list. A validation method ensures that at least three details are provided for the offer.

    Attributes:
        details (list of OfferDetailSerializer): A list of offer details.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """
        Validates that an offer contains at least 3 details.

        This method ensures that the number of details provided for the offer is at least 3, 
        raising a validation error if there are fewer.

        Args:
            value (list): The list of details provided for the offer.

        Returns:
            list: The validated details.

        Raises:
            serializers.ValidationError: If the number of details is less than 3.
        """
        if len(value) < 3:
            raise serializers.ValidationError('Ein Offer muss mindestens 3 Details enthalten.')
        return value

    def create(self, validated_data):
        """
        Creates a new offer and its associated details.

        This method creates an offer object and iterates through the provided details data to create
        associated OfferDetail objects.

        Args:
            validated_data (dict): The validated data for the offer.

        Returns:
            Offer: The newly created offer object.
        """
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        """
        Updates an existing offer and its associated details.

        This method updates an offer object, and if new details are provided, it either updates existing details
        or creates new ones.

        Args:
            instance (Offer): The offer instance to be updated.
            validated_data (dict): The validated data for updating the offer.

        Returns:
            Offer: The updated offer object.

        Raises:
            serializers.ValidationError: If an offer detail with a specified ID does not exist.
        """
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

        return instance


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offers and their details.

    This serializer is used when updating an offer, including its details. It allows partial updates
    and requires that at least one detail is associated with the offer.

    Attributes:
        details (OfferDetailPatchSerializer): A nested serializer for updating offer details.
    """
    details = OfferDetailPatchSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """
        Updates an offer and its details.

        This method updates the offer object and the associated details. If no existing detail is found
        for a specified offer_type, a validation error is raised.

        Args:
            instance (Offer): The offer instance to be updated.
            validated_data (dict): The validated data for updating the offer.

        Returns:
            Offer: The updated offer object.

        Raises:
            serializers.ValidationError: If no matching offer detail is found for the given offer_type.
        """
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
    details = OfferDetailGetSerializer(read_only=True, many=True)
    min_price = serializers.IntegerField()
    min_delivery_time = serializers.IntegerField()
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']