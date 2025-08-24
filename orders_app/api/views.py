from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from orders_app.models import Order
from .serializers import OrderListSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
