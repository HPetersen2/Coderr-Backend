from django.urls import path
from .views import ProfileListDetailView

urlpatterns = [
    path('profile/<int:pk>/', ProfileListDetailView.as_view()),
]