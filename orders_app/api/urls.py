from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderCountView, OrderCompletedCountView

urlpatterns = [
    # Route: /orders/ (GET for listing, POST for creating an order)
    path('orders/', OrderListCreateView.as_view()),

    # Route: /orders/<int:pk>/ (GET, PATCH, DELETE for a specific order by ID)
    path('orders/<int:pk>/', OrderDetailView.as_view()),

    # Route: /order-count/<int:business_user_id>/ (GET to retrieve the count of orders for a business user)
    path('order-count/<int:business_user_id>/', OrderCountView.as_view()),

    # Route: /completed-order-count/<int:business_user_id>/ (GET to retrieve the count of completed orders)
    path('completed-order-count/<int:business_user_id>/', OrderCompletedCountView.as_view()),
]
