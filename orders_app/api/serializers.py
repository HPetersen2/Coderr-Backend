from rest_framework import serializers
from orders_app.models import Order

class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with related offer details.

    This serializer is used for retrieving a list of orders, including fields related to the offer details.
    It serializes information such as the offer title, revisions, delivery time, features, and offer type.
    """

    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    features = serializers.ListField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type', 
            'status', 'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """
        Customize the representation of the order object to return additional
        offer details from the related `offer_detail` object.

        Args:
            instance (Order): The order instance to be serialized.

        Returns:
            dict: A dictionary representing the order along with its offer details.
        """
        representation = super().to_representation(instance)
        # Add additional details from the offer_detail
        representation['offer_detail'] = {
            'title': instance.offer_detail.title,
            'revisions': instance.offer_detail.revisions,
            'delivery_time_in_days': instance.offer_detail.delivery_time_in_days,
            'features': instance.offer_detail.features,
            'offer_type': instance.offer_detail.offer_type,
        }
        return representation

class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an order.

    This serializer is used for creating a new order by associating an `OfferDetail`
    with the `Order` and automatically setting customer and business users based on the offer details.
    """

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.model.offer_detail.field.related_model.objects.all(),
        source='offer_detail',
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def create(self, validated_data):
        """
        Create a new order instance.

        This method is used to create a new order based on the provided offer detail.
        The customer user is automatically set to the current authenticated user,
        and the business user is set to the user associated with the offer.

        Args:
            validated_data (dict): The validated data for the new order.

        Returns:
            Order: The newly created order instance.
        """
        offer_detail = validated_data['offer_detail']
        validated_data['customer_user'] = self.context['request'].user  # Set customer as current user
        validated_data['business_user'] = offer_detail.offer.user  # Set business user from the offer's user
        validated_data['price'] = offer_detail.price  # Set price from offer detail
        return super().create(validated_data)

class OrderCountSerializer(serializers.Serializer):
    """
    Serializer for returning the count of orders.

    This serializer is used to return the total number of orders for a given context or filter.
    """

    order_count = serializers.IntegerField()

class OrderCompletedCountSerializer(serializers.Serializer):
    """
    Serializer for returning the count of completed orders.

    This serializer is used to return the number of completed orders.
    It can be useful for analytics or status reporting.
    """

    completed_order_count = serializers.IntegerField()
