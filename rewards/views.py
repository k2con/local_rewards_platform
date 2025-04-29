from rest_framework import viewsets
from .models import Reward, RewardBrand, PurchaseDetail
from .serializers import RewardSerializer, RewardBrandSerializer, PurchaseDetailSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

class RewardBrandViewSet(viewsets.ModelViewSet):
    queryset = RewardBrand.objects.all()
    serializer_class = RewardBrandSerializer

class PurchaseDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseDetail.objects.all()
    serializer_class = PurchaseDetailSerializer
