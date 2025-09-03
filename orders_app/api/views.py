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
    - `GET`: Lists orders based on the user's profile (business or customer).
    - `POST`: Creates new orders for the authenticated user (customer or business).
    """
    permission_classes = [IsAuthenticated, IsCustomerUser]
    pagination_class = None

    def get_queryset(self):
        """
        Returns orders based on the authenticated user's profile type.
        - Business users see orders related to their business.
        - Customer users see orders related to them.
        """
        user = self.request.user
        if user.userprofile.type == 'business':
            return Order.objects.filter(business_user=user).select_related('offer_detail')
        return Order.objects.filter(customer_user=user).select_related('offer_detail')

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class:
        - `POST` uses `OrderCreateSerializer` for order creation.
        - Other methods use `OrderListSerializer` for listing orders.
        """
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def perform_create(self, serializer):
        """
        Saves the new order and prepares the response serializer for listing.
        """
        order = serializer.save()
        self._response_serializer = OrderCreateSerializer(order, context=self.get_serializer_context())

    def create(self, request, *args, **kwargs):
        """
        Handles order creation and returns the new order's details in the response.
        """
        response = super().create(request, *args, **kwargs)
        if hasattr(self, '_response_serializer'):
            response.data = self._response_serializer.data
        return response


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, or deleting a specific order.
    """
    queryset = Order.objects.filter()
    serializer_class = OrderListSerializer

    def get_permissions(self):
        """
        Returns the appropriate permissions:
        - `PATCH` requires business user permissions.
        - `DELETE` requires admin user permissions.
        """
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsBusinessUser]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderCountView(generics.GenericAPIView):
    """
    A view for getting the total count of orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Retrieves the order count for a business user by ID.
        Returns the count of orders in 'in_progress' status.
        """
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        serializer = self.get_serializer({'order_count': order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCompletedCountView(generics.GenericAPIView):
    """
    A view for getting the count of completed orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCompletedCountSerializer

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Retrieves the count of completed orders for a business user by ID.
        Returns the count of orders in 'completed' status.
        """
        business_user = get_object_or_404(get_user_model(), id=business_user_id, userprofile__type='business')
        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        serializer = self.get_serializer({'completed_order_count': completed_order_count})
        return Response(serializer.data, status=status.HTTP_200_OK)

