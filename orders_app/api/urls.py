from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderCountView, OrderCompletedCountView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view()),
    path('completed-order-count/<int:business_user_id>/', OrderCompletedCountView.as_view()),
]