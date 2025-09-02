import django_filters
from reviews_app.models import Review

class ReviewFilter(django_filters.FilterSet):
    """
    A filter set for filtering reviews based on specific criteria, such as the business user
    and the reviewer. This allows for more fine-grained control over which reviews are returned
    in the query results.

    Attributes:
        business_user_id (NumberFilter): A filter to match reviews based on the `business_user` field.
        reviewer_id (NumberFilter): A filter to match reviews based on the `reviewer` field.
    
    Meta:
        model (Review): The model to which this filter set is applied.
        fields (list): The list of fields that can be filtered, including `business_user_id` and `reviewer_id`.
    """
    business_user_id = django_filters.NumberFilter(field_name='business_user', lookup_expr='exact')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']
