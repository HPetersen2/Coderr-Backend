from django.urls import path
from .views import ReviewsView, ReviewDetailView

# URL pattern for the reviews-related views.
urlpatterns = [
    # The first path maps to the ReviewsView to handle requests related to listing and creating reviews.
    path('reviews/', ReviewsView.as_view()),
    # The second path maps to the ReviewDetailView to handle requests related to retrieving, updating, or deleting a specific review.
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),  # Retrieve, update, or delete a specific review
]
