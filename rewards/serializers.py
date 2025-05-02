from rest_framework import serializers
from .models import BrandsCategory, Brand, Country, PurchaseDetail, BrandCountry, Reward, Currency, Price

class BrandsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandsCategory
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    category = BrandsCategorySerializer()

    class Meta:
        model = Brand
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class BrandCountrySerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    country = CountrySerializer()
    purchase = PurchaseDetailSerializer()

    class Meta:
        model = BrandCountry
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Price
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    brand_country = BrandCountrySerializer()
    prices = PriceSerializer(many=True)  # ← porque Reward tiene una relación one-to-many con Price

    class Meta:
        model = Reward
        fields = '__all__'
