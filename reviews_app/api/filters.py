import django_filters
from reviews_app.models import Review

class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name='business_user', lookup_expr='exact')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']