from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Status and Type Choices
STATUS_CHOICES = [
    ('Active', _('Active')),
    ('Inactive', _('Inactive')),
    ('Pending', _('Pending')),
]

PRICE_TYPE_CHOICES = [
    ('Range', _('Range')),
    ('Fixed', _('Fixed')),
    ('Multivalue', _('Multivalue')),
]

class BrandsCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name="Category Title")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=500)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    verified = models.BooleanField(default=False)
    category = models.ForeignKey(BrandsCategory, on_delete=models.CASCADE, related_name='brands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=10)
    phone_prefix = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class BrandCountry(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand.id}) {self.brand.name} - {self.country.name}"

class PurchaseDetail(models.Model):
    brand_country = models.OneToOneField(BrandCountry, on_delete=models.CASCADE)
    where_to_buy = models.TextField(null=True, blank=True)
    how_to_buy = models.TextField(null=True, blank=True)
    how_to_redeem = models.TextField(null=True, blank=True)
    bulk_detail = models.TextField(null=True, blank=True)
    process_duration_detail = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    merchant_coverage_detail = models.TextField(null=True, blank=True)
    conditions = models.TextField(null=True, blank=True)
    validity = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Reward(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    brand_country = models.OneToOneField(BrandCountry, on_delete=models.CASCADE)
    reward_type = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Currency(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.iso_code

class Price(models.Model):
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE, related_name='prices')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES)
    value_min = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)#None
    value_max = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)#None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)