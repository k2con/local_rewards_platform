from rest_framework import serializers
from .models import Reward, RewardBrand, PurchaseDetail

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class RewardBrandSerializer(serializers.ModelSerializer):
    purchase_detail = PurchaseDetailSerializer()

    class Meta:
        model = RewardBrand
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    reward_brand = RewardBrandSerializer()

    class Meta:
        model = Reward
        fields = '__all__'
