import django_filters
from offers_app.models import Offer

class OfferFilter(django_filters.FilterSet):
    """
    Filter offers by creator ID, minimum price, and maximum delivery time using django_filters.
    
    Filters:
        creator_id: Filters offers by the creator's user ID.
        min_price: Filters offers with a minimum price greater than or equal to the specified value.
        max_delivery_time: Filters offers with a maximum delivery time less than or equal to the specified value.
    """
    
    creator_id = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.filter(min_delivery_time__lte=value)

