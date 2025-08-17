from django.urls import path
from .views import ProfileDetailView, ProfileBusinessList

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view()),
    path('profiles/business/', ProfileBusinessList.as_view()),
]