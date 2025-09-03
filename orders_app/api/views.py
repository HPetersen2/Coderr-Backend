from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from orders_app.models import Order
from .permissions import IsCustomerUser, IsBusinessUser
from .serializers import OrderListSerializer, OrderCreateSerializer, OrderCountSerializer, OrderCompletedCountSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    """
    A view for listing and creating orders. 
    - Supports `GET` to list orders based on the user's profile type (either business or customer).
    - Supports `POST` to create new orders for the authenticated user (either customer or business).
    """
    permission_classes = [IsAuthenticated, IsCustomerUser]
    pagination_class = None

    def get_queryset(self):
        """
        Returns the queryset of orders based on the authenticated user's profile type.
        - If the user is a 'business' user, orders related to the business are returned.
        - If the user is a 'customer', orders related to the customer are returned.
        """
        user = self.request.user
        if user.userprofile.type == 'business':
            return Order.objects.filter(business_user=user).select_related('offer_detail')
        return Order.objects.filter(customer_user=user).select_related('offer_detail')

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        - `POST` method uses the OrderCreateSerializer for creating orders.
        - Other methods use the OrderListSerializer for listing orders.
        """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def perform_create(self, serializer):
        """
        Saves the newly created order and prepares a response serializer for the list view.
        """
        order = serializer.save()
        self._response_serializer = OrderCreateSerializer(order, context=self.get_serializer_context())

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of an order.
        - After creating an order, the response data is updated with the new order details.
        """
        response = super().create(request, *args, **kwargs)
        if hasattr(self, '_response_serializer'):
            response.data = self._response_serializer.data
        return response

    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a specific order.
    """
    queryset = Order.objects.filter()
    serializer_class = OrderListSerializer

    def get_permissions(self):
        """
        Returns the appropriate permission classes based on the HTTP method.
        - `PATCH` method requires business user permissions.
        - `DELETE` method requires admin user permissions.
        """
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsBusinessUser]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
class OrderCountView(generics.GenericAPIView):
    """
    A view to get the total count of orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Retrieves the order count for the given business user ID.
        - Only counts orders related to the business user and returns the count in the response.
        """
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')
        
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        serializer = self.get_serializer({'order_count': order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderCompletedCountView(generics.GenericAPIView):
    """
    A view to get the count of completed orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCompletedCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Retrieves the count of completed orders for the given business user ID.
        - Filters orders by the 'completed' status and returns the count in the response.
        """
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')

        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        serializer = self.get_serializer({'completed_order_count': completed_order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
