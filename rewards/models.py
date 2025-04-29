from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError

PRICE_CHOICES = [
    ('fixed', _('Fixed')),
    ('multi-value', _('Multi Value')),
    ('range', _('Range')),
    ('custom', _('Custom')),
]
STATUS_CHOICES = [
    ('active', _('Active')),
    ('inactive', _('Inactive')),
    ('pending', _('Pending')),
]

class PurchaseDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    where_to_buy = models.TextField(blank=True, null=True)
    how_to_buy = models.TextField(blank=True, null=True)
    how_to_redeem = models.TextField(blank=True, null=True)
    bulk_detail = models.TextField(blank=True, null=True)
    process_duration_detail = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    merchant_coverage_detail = models.TextField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    validity = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'purchase_details'

class RewardBrand(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    slug = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    website_url = models.URLField(max_length=2048, blank=True, null=True)  # Increased max_length
    purchase_detail = models.ForeignKey(PurchaseDetail,on_delete=models.SET_NULL,related_name='reward_brands',blank=True,null=True)
    class Meta:
        db_table = 'reward_brands'

class Reward(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    slug = models.CharField(max_length=255, unique=True)
    category_slug = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)

    price_type = models.CharField(max_length=20, choices=PRICE_CHOICES, default='fixed')
    price = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone_number = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    reward_brand = models.ForeignKey(RewardBrand, on_delete=models.CASCADE, related_name='rewards')
    

    class Meta:
        db_table = 'rewards'
