from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from orders_app.models import Order
from .serializers import OrderListSerializer

class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.userprofile.type == 'business':
            raise PermissionDenied(detail='Business users cannot view orders.')
        else:
            return Order.objects.filter(customer_user=self.request.user)
    