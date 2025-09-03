from django.urls import path
from offers_app.api.views import OfferListView, OfferView, OfferDetailView

urlpatterns = [
    # Route for listing all offers.
    # Maps 'offers/' to the OfferListView for a list of all available offers.
    path('offers/', OfferListView.as_view()),

    # Route for viewing or updating a specific offer by its 'pk'.
    # Maps 'offers/<int:pk>/' to the OfferView.
    path('offers/<int:pk>/', OfferView.as_view(), name='offer'),

    # Route for viewing or updating offer details by 'pk'.
    # Maps 'offerdetails/<int:pk>/' to the OfferDetailView.
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]

