"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    # URL pattern to include API routes from the 'auth_app' for authentication-related views.
    # This includes routes like user registration, login, and other authentication features.
    path('', include('auth_app.api.urls')),

    # URL pattern to include API routes from the 'offers_app' for handling offer-related views.
    # This will include routes for creating, listing, and managing offers in the system.
    path('', include('offers_app.api.urls')),

    # URL pattern to include API routes from the 'orders_app' for order-related views.
    # This includes routes for creating and managing orders placed by customers.
    path('', include('orders_app.api.urls')),

    # URL pattern to include API routes from the 'reviews_app' for review-related views.
    # This will include routes for creating and managing reviews for businesses.
    path('', include('reviews_app.api.urls')),

    # URL pattern to include API routes from the 'stats_app' for statistics-related views.
    # This includes routes for fetching system-wide statistics such as review counts, ratings, etc.
    path('', include('stats_app.api.urls'))
]
