import django_filters
from offers_app.models import Offer

class OfferFilter(django_filters.FilterSet):
    """
    Filter class for filtering Offer objects based on specific criteria.
    This class allows filtering offers by creator ID, minimum price, and maximum delivery time.
    It leverages the django_filters library to provide an easy and customizable filtering interface for offer-related data.
    """

    creator_id = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    """
    Filter for selecting offers created by a specific user based on their user ID.
    The 'user__id' lookup refers to the ID field of the related User model.
    The 'exact' lookup expression ensures that only offers from the user with the exact given ID are included in the result.
    """

    min_price = django_filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    """
    Filter for selecting offers where the minimum price is greater than or equal to the specified value.
    The 'min_price' field is used, and the 'gte' (greater than or equal) lookup expression ensures that only offers
    with a minimum price greater than or equal to the specified value are included.
    """

    max_delivery_time = django_filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')
    """
    Filter for selecting offers where the minimum delivery time is less than or equal to the specified value.
    The 'min_delivery_time' field is used, and the 'lte' (less than or equal) lookup expression ensures that only
    offers with a delivery time less than or equal to the specified value are included.
    """

    class Meta:
        model = Offer
        """
        Specifies the model that this filter is associated with.
        The filter will apply to the 'Offer' model.
        """
        fields = ['creator_id']
        """
        Defines the fields that can be used for filtering.
        In this case, only 'creator_id' is specified in the Meta class.
        Additional fields, such as min_price and max_delivery_time, are handled manually.
        """

    def filter_min_price(self, queryset, name, value):
        """
        Custom filter for the 'min_price' field.
        Filters the queryset to include only offers where the 'min_price' is greater than or equal to the specified value.

        Args:
            queryset (QuerySet): The original queryset to filter.
            name (str): The name of the filter field.
            value (int or float): The value to filter the 'min_price' field.

        Returns:
            QuerySet: The filtered queryset.
        """
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Custom filter for the 'max_delivery_time' field.
        Filters the queryset to include only offers where the 'min_delivery_time' is less than or equal to the specified value.

        Args:
            queryset (QuerySet): The original queryset to filter.
            name (str): The name of the filter field.
            value (int): The value to filter the 'min_delivery_time' field.

        Returns:
            QuerySet: The filtered queryset.
        """
        return queryset.filter(min_delivery_time__lte=value)
