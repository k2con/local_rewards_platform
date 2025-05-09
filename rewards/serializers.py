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

# class PurchaseDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseDetail
#         fields = '__all__'

# class BrandCountrySerializer(serializers.ModelSerializer):
#     brand = BrandSerializer()
#     country = CountrySerializer()
#     purchase = PurchaseDetailSerializer()

#     class Meta:
#         model = BrandCountry
#         fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class BrandCountrySerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    country = CountrySerializer()
    purchase = serializers.SerializerMethodField()
    contact_phone_number = serializers.SerializerMethodField()


    class Meta:
        model = BrandCountry
        fields = '__all__'  # puedes mantener '__all__' pero el campo `purchase` será adicional

    def get_purchase(self, obj):
        try:
            # Si agregaste related_name="purchase_detail"
            purchase = obj.purchase_detail
            return PurchaseDetailSerializer(purchase).data
        except PurchaseDetail.DoesNotExist:
            return None
        except AttributeError:
            # Si no agregaste related_name
            try:
                purchase = PurchaseDetail.objects.get(brand_country=obj)
                return PurchaseDetailSerializer(purchase).data
            except PurchaseDetail.DoesNotExist:
                return None
    def get_contact_phone_number(self, obj):
        try:
            phone = obj.contact_phone_number
            prefix = obj.country.phone_prefix
            if prefix and phone:
                return f'+{prefix}{phone}'
            return phone
        except AttributeError:
            return phone



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
    
