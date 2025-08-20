from django.urls import path
from .views import ProfileDetailView, ProfileBusinessList, ProfileCustomerList

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view()),
    path('profiles/business/', ProfileBusinessList.as_view()),
    path('profiles/customer/', ProfileCustomerList.as_view()),
]