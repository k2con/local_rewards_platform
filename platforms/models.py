from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class Platform(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, blank=True, null=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='platforms')
    purchase_detail = models.ForeignKey('purchases.PurchaseDetail', on_delete=models.SET_NULL, null=True, blank=True, related_name='platforms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'platforms'