from django.urls import path
from offers_app.api.views import OfferListView, OfferView, OfferDetailView

urlpatterns = [
    # Route for listing all offers.
    # Maps the URL path 'offers/' to the OfferListView class-based view.
    # This view is responsible for returning a list of all available offers.
    path('offers/', OfferListView.as_view()),

    # Route for viewing or updating a specific offer.
    # Maps the URL path 'offers/<int:pk>/' to the OfferView class-based view.
    # The 'pk' parameter allows access to a specific offer by its primary key.
    # Named 'offer' for easy reference in templates or reverse lookups.
    path('offers/<int:pk>/', OfferView.as_view(), name='offer'),

    # Route for viewing or updating offer details.
    # Maps the URL path 'offerdetails/<int:pk>/' to the OfferDetailView class-based view.
    # The 'pk' parameter allows access to a specific offer detail by its primary key.
    # Named 'offer-detail' for consistent reference throughout the project.
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]
