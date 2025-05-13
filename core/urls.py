from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.shortcuts import redirect
from rewards.views import RewardViewSet #BrandsCategoryViewSet, BrandViewSet, CountryViewSet, PurchaseDetailViewSet, BrandCountryViewSet, CurrencyViewSet, PriceViewSet, RewardViewSet

router = routers.DefaultRouter()
router.register(r'rewards', RewardViewSet)
# router.register(r'brands-categories', BrandsCategoryViewSet)
# router.register(r'brands', BrandViewSet)
# router.register(r'countries', CountryViewSet)
# router.register(r'purchase-details', PurchaseDetailViewSet)
# router.register(r'brand-countries', BrandCountryViewSet)
# router.register(r'currencies', CurrencyViewSet) 
# router.register(r'prices', PriceViewSet)

urlpatterns = [
    path('', lambda request: redirect('/admin/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]