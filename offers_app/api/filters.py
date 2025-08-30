import django_filters
from offers_app.models import Offer

class OfferFilter(django_filters.FilterSet):
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