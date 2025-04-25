from django.db import models
from django.utils.translation import gettext_lazy as _

class PurchaseDetail(models.Model):
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
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Purchase Detail #{self.id}"

    class Meta:
        db_table = 'purchase_details'

    @classmethod
    def handle_update_or_create(cls, purchase_detail_id: int = None, data: dict = None):
        if purchase_detail_id:
            try:
                purchase_detail = cls.objects.get(pk=purchase_detail_id)
                for key, value in data.items():
                    setattr(purchase_detail, key, value)
                purchase_detail.save()
                return purchase_detail
            except cls.DoesNotExist:
                return None
        else:
            return cls.objects.create(**data)