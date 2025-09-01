from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from orders_app.models import Order
from .serializers import OrderListSerializer

class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.userprofile.type == 'business':
            return Order.objects.filter(business_user=self.request.user)
        else:
            return Order.objects.filter(customer_user=self.request.user)
    