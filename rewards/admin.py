from django.contrib import admin
from rewards.models import (
    BrandsCategory, Brand, Country,
    PurchaseDetail, BrandCountry, Reward,
    Currency, Price
)

# 
@admin.register(BrandsCategory)  
class BrandsCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['deleted_at']

#
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code']
    readonly_fields = ['deleted_at']
    ordering = ['name']

#
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'status_display', 'category']
    search_fields = ['name', 'website_url']
    list_filter = ['category']
    readonly_fields = ['deleted_at']
    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"


#
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'phone_prefix']
    search_fields = ['name', 'iso_code']
    list_filter = ['created_at']
    ordering = ['name']
    readonly_fields = ['deleted_at']


# 
class PriceInline(admin.TabularInline):
    model = Price
    extra = 1
    readonly_fields = ['deleted_at']


# 
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    inlines = [PriceInline]
    list_display= ['brand_country', 'reward_type', 'status_display']
    readonly_fields = ['deleted_at']

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"
# 
class PurchaseDetailInline(admin.StackedInline):
    model = PurchaseDetail
    extra = 1

# 
@admin.register(BrandCountry)
class BrandCountryAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInline]
    list_display = ['brand', 'country']
    search_fields = ['brand__name']
    list_filter = ['country']
    readonly_fields = ['deleted_at']

