import django_filters
from .models import Reward

class RewardFilter(django_filters.FilterSet):
    brandName = django_filters.CharFilter(field_name='brand_country__brand__name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='brand_country__country__iso_code', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='brand_country__brand__category__title', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    currency = django_filters.CharFilter(field_name='prices__currency__iso_code', lookup_expr='iexact')
    priceMin = django_filters.CharFilter(field_name='prices__value_min', lookup_expr='iexact')
    priceMax = django_filters.CharFilter(field_name='prices__value_max', lookup_expr='iexact')
    # Rango de precios
    # priceMin = django_filters.NumberFilter(field_name='prices__value_min', lookup_expr='gte')
    # priceMax = django_filters.NumberFilter(field_name='prices__value_max', lookup_expr='lte')


    class Meta:
        model = Reward
        fields = ['brandName', 'country', 'category', 'status', 'currency', 'priceMin', 'priceMax']
