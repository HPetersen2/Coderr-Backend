from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from orders_app.models import Order
from .permissions import IsCustomerUser, IsBusinessUser
from .serializers import OrderListSerializer, OrderCreateSerializer, OrderCountSerializer, OrderCompletedCountSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomerUser]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.userprofile.type == 'business':
            return Order.objects.filter(business_user=user).select_related('offer_detail')
        return Order.objects.filter(customer_user=user).select_related('offer_detail')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        self._response_serializer = OrderListSerializer(order, context=self.get_serializer_context())

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if hasattr(self, '_response_serializer'):
            response.data = self._response_serializer.data
        return response
    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.filter()
    serializer_class = OrderListSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsBusinessUser]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated ,IsAdminUser]
        return [permission() for permission in permission_classes]
    
class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')
        
        order_count = Order.objects.filter(business_user=business_user).count()
        serializer = self.get_serializer({'order_count': order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderCompletedCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCompletedCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')

        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        serializer = self.get_serializer({'completed_order_count': completed_order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)