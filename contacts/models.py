from django.db import models
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    website = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)    
    phone_country_code = models.CharField(max_length=5, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or self.email or f"Contacto #{self.id}"

    class Meta:
        db_table = 'contacts' 

    @classmethod
    def handle_update_or_create(cls, contact_id: int = None, data: dict = None):
        if contact_id:
            try:
                contact = cls.objects.get(pk=contact_id)
                for key, value in data.items():
                    setattr(contact, key, value)
                contact.save()
                return contact
            except cls.DoesNotExist:
                return None 
        else:
            return cls.objects.create(**data)