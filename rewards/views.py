from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Reward# BrandsCategory, Brand,Country,PurchaseDetail,BrandCountry,Currency,Price
from .serializers import RewardSerializer#BrandsCategorySerializer, BrandSerializer, CountrySerializer, PurchaseDetailSerializer, BrandCountrySerializer, CurrencySerializer, PriceSerializer
from .filters import RewardFilter

# class BrandsCategoryViewSet(viewsets.ModelViewSet):
#     queryset = BrandsCategory.objects.all()
#     serializer_class = BrandsCategorySerializer
#
# class BrandViewSet(viewsets.ModelViewSet):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer

# class CountryViewSet(viewsets.ModelViewSet):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer

# class PurchaseDetailViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseDetail.objects.all()
#     serializer_class = PurchaseDetailSerializer

# class BrandCountryViewSet(viewsets.ModelViewSet):
#     queryset = BrandCountry.objects.all()
#     serializer_class = BrandCountrySerializer

# class CurrencyViewSet(viewsets.ModelViewSet):
#     queryset = Currency.objects.all()
#     serializer_class = CurrencySerializer

# class PriceViewSet(viewsets.ModelViewSet):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer


class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['status', 'brand_country__brand__name'] 
    filterset_class = RewardFilter
