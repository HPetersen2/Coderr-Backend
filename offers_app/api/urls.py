from django.urls import path
from offers_app.api.views import OfferListView, OfferView, OfferDetailView

urlpatterns = [
    path('offers/', OfferListView.as_view()),
    path('offers/<int:pk>/', OfferView.as_view(), name='offer'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]