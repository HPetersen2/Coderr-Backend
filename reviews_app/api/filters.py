import django_filters
from reviews_app.models import Review

class ReviewFilter(django_filters.FilterSet):
    """
    A filter set for filtering reviews based on business user and reviewer.

    Attributes:
        business_user_id (NumberFilter): Filters reviews by the `business_user` field.
        reviewer_id (NumberFilter): Filters reviews by the `reviewer` field.
    
    """
    business_user_id = django_filters.NumberFilter(field_name='business_user', lookup_expr='exact')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']

