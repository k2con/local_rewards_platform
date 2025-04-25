from django.db import models
from django.utils.translation import gettext_lazy as _

class RewardType(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    brands = models.ManyToManyField('reward_brands.RewardBrand', related_name='reward_type_brands') 


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'reward_types'

    @classmethod
    def to_searchable_array(cls):
        return [{'value': reward_type.id, 'label': reward_type.name}
                for reward_type in cls.objects.order_by('name').all()]