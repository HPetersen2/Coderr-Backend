from django.urls import path
from offers_app.api.views import OfferListView, OfferView, OfferDetailView

urlpatterns = [
    # Maps 'offers/' to the OfferListView for a list of all available offers.
    path('offers/', OfferListView.as_view()),

    # Maps 'offers/<int:pk>/' to the OfferView.
    path('offers/<int:pk>/', OfferView.as_view(), name='offer'),

    # Maps 'offerdetails/<int:pk>/' to the OfferDetailView.
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]

