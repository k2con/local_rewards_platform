from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

# Definición de Enums 
class ModelStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    ARCHIVED = 'archived', _('Archived')

class PriceType(models.TextChoices):
    FIXED = 'fixed', _('Fixed')
    MULTI_VALUE = 'multi-value', _('Multi Value')
    RANGE = 'range', _('Range')
    CUSTOM = 'custom', _('Custom')

class Reward(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()
    reward_brand = models.ForeignKey('reward_brands.RewardBrand', on_delete=models.CASCADE, related_name='reward_set')
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name='rewards')
    purchase_detail = models.ForeignKey('purchases.PurchaseDetail', on_delete=models.CASCADE, null=True, blank=True, related_name='rewards')
    country = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    price_type = models.CharField(
        max_length=20,
        choices=PriceType.choices,
        default=PriceType.FIXED
    )
    price = models.JSONField(encoder=DjangoJSONEncoder)
    status = models.CharField(
        max_length=10,
        choices=ModelStatus.choices,
        default=ModelStatus.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def formattedPrice(self):
        if self.price_type == PriceType.FIXED:
            price = self.price[0] if isinstance(self.price, list) and self.price else 0
            return f"{self.currency} {price:,.2f}"
        elif self.price_type in [PriceType.MULTI_VALUE, PriceType.CUSTOM]:
            return f"{self.currency} {', '.join(map(str, self.price))}"
        elif self.price_type == PriceType.RANGE:
            return f"{self.currency} {' - '.join(map(str, self.price))}"
        return self.price

    def __str__(self):
        return self.slug
