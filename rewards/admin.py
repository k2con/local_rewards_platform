from django.contrib import admin
from rewards.models import BrandsCategory, Brand,Country,PurchaseDetail,BrandCountry,Reward,Currency,Price

# Register your models here.

admin.site.register(BrandsCategory)
admin.site.register(Brand)
admin.site.register(Country)
admin.site.register(PurchaseDetail)
admin.site.register(BrandCountry)   
admin.site.register(Reward)
admin.site.register(Currency)
admin.site.register(Price)