from rest_framework import generics
from orders_app.models import Order
from .serializers import OrderListSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
