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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # URL pattern for the Django admin site.
    # This URL route allows access to the Django admin panel for site administrators.
    path('admin/', admin.site.urls),

    # URL pattern for the API endpoints.
    # This route includes the URL configurations from the 'core.api_urls' module.
    # The API URLs are handled by the 'core' app and provide access to the API views.
    path('api/', include('core.api_urls'))
]

