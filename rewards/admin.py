from django.contrib import admin
from rewards.models import BrandsCategory, Brand,Country,PurchaseDetail,BrandCountry,Reward,Currency,Price

# Register your models here.

admin.site.register(BrandsCategory)
admin.site.register(Brand)
admin.site.register(Country)
# admin.site.register(PurchaseDetail)
# admin.site.register(BrandCountry)  
# admin.site.register(Reward)
admin.site.register(Currency)
# admin.site.register(Price)

class PriceInline(admin.TabularInline):  # StackedInline
    model = Price
    extra = 1

class RewardAdmin(admin.ModelAdmin):
    inlines = [PriceInline]

admin.site.register(Reward, RewardAdmin)



class PurchaseDetailInline(admin.StackedInline):
    model = PurchaseDetail
    extra = 1

class BrandCountryAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInline]

admin.site.register(BrandCountry, BrandCountryAdmin)    