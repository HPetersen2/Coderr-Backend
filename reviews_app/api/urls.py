from django.urls import path
from .views import ReviewsView, ReviewDetailView

urlpatterns = [
    # URL pattern for the reviews-related views.
    # The first path maps to the ReviewsView to handle requests related to listing and creating reviews.
    # The second path maps to the ReviewDetailView to handle requests related to retrieving, updating, or deleting a specific review.
    path('reviews/', ReviewsView.as_view()),  # List and create reviews
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),  # Retrieve, update, or delete a specific review
]
