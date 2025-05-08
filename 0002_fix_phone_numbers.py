from django.db import migrations

def remove_dot_zero_from_phone_numbers(apps, schema_editor):
    print("test")
    BrandCountry = apps.get_model('rewards', 'BrandCountry')

    for entry in BrandCountry.objects.all():
        phone = entry.contact_phone_number
        if phone and phone.endswith('.0'):
            # Elimina el .0 al final
            entry.contact_phone_number = phone[:-2]
            entry.save(update_fields=["contact_phone_number"])

def noop_reverse(apps, schema_editor):
    # Esta función no hace nada, solo permite revertir sin error
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_dot_zero_from_phone_numbers, reverse_code=noop_reverse),
    ]


