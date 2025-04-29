from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rewards.views import RewardViewSet, RewardBrandViewSet, PurchaseDetailViewSet

router = routers.DefaultRouter()
router.register(r'rewards', RewardViewSet)
router.register(r'reward-brands', RewardBrandViewSet)
router.register(r'purchase-details', PurchaseDetailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]