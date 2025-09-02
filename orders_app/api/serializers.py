from rest_framework import serializers
from orders_app.models import Order

class OrderListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    features = serializers.ListField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.model.offer_detail.field.related_model.objects.all(),
        source='offer_detail'
    )

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def create(self, validated_data):
        offer_detail = validated_data['offer_detail']
        validated_data['customer_user'] = self.context['request'].user
        validated_data['business_user'] = offer_detail.offer.user
        validated_data['price'] = offer_detail.price
        return super().create(validated_data)
    
class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField()

class OrderCompletedCountSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField()