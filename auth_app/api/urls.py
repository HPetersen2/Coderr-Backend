from django.urls import path, include
from .views import UserProfileCreateView, LoginView, ProfileDetailView, ProfileBusinessList, ProfileCustomerList

# URL patterns for user-related endpoints
urlpatterns = [
    # User registration route
    # Maps 'registration/' to UserProfileCreateView (Named 'user-register')
    path('registration/', UserProfileCreateView.as_view(), name='user-register'),

    # User login route
    # Maps 'login/' to LoginView (Named 'user-login')
    path('login/', LoginView.as_view(), name='user-login'),

    # View/update specific user profile by primary key (pk)
    path('profile/<int:pk>/', ProfileDetailView.as_view()),

    # List of business-type user profiles
    path('profiles/business/', ProfileBusinessList.as_view()),

    # List of customer-type user profiles
    path('profiles/customer/', ProfileCustomerList.as_view()),
]

