from django.urls import path
from offers_app.api.views import OfferListView, OfferDetailView

urlpatterns = [
    path('offers/', OfferListView.as_view()),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]