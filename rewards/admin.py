from django.contrib import admin
from rewards.models import RewardBrand, Reward, PurchaseDetail

# Register your models here.

admin.site.register(RewardBrand)
admin.site.register(Reward) 
admin.site.register(PurchaseDetail)