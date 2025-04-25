from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

# En RewardBrand
class RewardBrand(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey('platforms.Platform', on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_brands')
    contact = models.ForeignKey('contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_brands')
    purchase_detail = models.ForeignKey('purchases.PurchaseDetail', on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_brands')
    verified = models.BooleanField(default=False)
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, blank=True, null=True) 
    type = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Relaciones ManyToMany con related_name para evitar el conflicto
    categories = models.ManyToManyField('rewards_categories.RewardCategory', related_name='reward_brands_categories')
    types = models.ManyToManyField('rewards_types.RewardType', related_name='reward_brands_types')

    # Relación con ForeignKey (uno a muchos)
    rewards = models.ForeignKey('rewards.Reward', on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_brands') 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'reward_brands'


