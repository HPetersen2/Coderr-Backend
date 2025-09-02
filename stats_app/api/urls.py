from django.urls import path, include
from .views import BaseInfoView

urlpatterns = [
    # URL pattern for the BaseInfoView.
    # This view returns basic system statistics such as the total number of reviews, 
    # average rating, number of business profiles, and the number of offers in the system.
    path('base-info/', BaseInfoView.as_view(), name='base-info'),  # Get system statistics
]