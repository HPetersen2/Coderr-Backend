from django.urls import path, include
from .views import UserProfileCreateView, LoginView, ProfileDetailView, ProfileBusinessList, ProfileCustomerList

# URL patterns define the routing for the user-related endpoints.
urlpatterns = [
    # Route for user registration.
    # Maps the URL path 'registration/' to the UserProfileCreateView class-based view.
    # Named 'user-register' for easy reference in templates or reverse lookups.
    path('registration/', UserProfileCreateView.as_view(), name='user-register'),

    # Route for user login.
    # Maps the URL path 'login/' to the LoginView class-based view.
    # Named 'user-login' for consistent reference throughout the project.
    path('login/', LoginView.as_view(), name='user-login'),

    # Route for viewing or updating a specific user profile.
    # Maps the URL path 'profile/<int:pk>/' to the ProfileDetailView class-based view,
    # where 'pk' is the primary key of the user profile being accessed.
    path('profile/<int:pk>/', ProfileDetailView.as_view()),

    # Route for viewing a list of business-type user profiles.
    # Maps the URL path 'profiles/business/' to the ProfileBusinessList class-based view.
    path('profiles/business/', ProfileBusinessList.as_view()),

    # Route for viewing a list of customer-type user profiles.
    # Maps the URL path 'profiles/customer/' to the ProfileCustomerList class-based view.
    path('profiles/customer/', ProfileCustomerList.as_view()),
]
