from django.urls import path
from .views import ReviewsView, ReviewDetailView

urlpatterns = [
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),
]