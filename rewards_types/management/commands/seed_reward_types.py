from django.core.management.base import BaseCommand
from rewards_types.models import RewardType

class Command(BaseCommand):
    help = 'Seed initial reward types into the database'

    def handle(self, *args, **kwargs):
        types = [
            {'slug': 'gift-card', 'name': 'Gift Card'},
            {'slug': 'reward-link', 'name': 'Reward Link'},
            {'slug': 'card', 'name': 'Card'},
            {'slug': 'cash-coupons', 'name': 'Cash Coupons'},
            {'slug': 'cell-top-up', 'name': 'Cell Top Up Only'},
            {'slug': 'certificate-voucher', 'name': 'Certificate / Voucher'},
            {'slug': 'day-passes', 'name': 'Day Passes'},
            {'slug': 'digital', 'name': 'Digital'},
            {'slug': 'digital-physical', 'name': 'Digital / Physical'},
            {'slug': 'digital-printed', 'name': 'Digital or printer'},
            {'slug': 'digital-ecard', 'name': 'Digital/E-card'},
            {'slug': 'fisica', 'name': 'Fisica'},
            {'slug': 'fuel-voucher', 'name': 'Fuel Voucher'},
            {'slug': 'mobile-credit', 'name': 'Mobile Credit'},
            {'slug': 'na', 'name': 'N/A'},
            {'slug': 'not-available', 'name': 'Not Available'},
            {'slug': 'physical', 'name': 'Physical'},
            {'slug': 'voucher', 'name': 'Voucher'},
            {'slug': 'voucher-physical-digital', 'name': 'Voucher - Physical / Digital'},
        ]

        for t in types:
            obj, created = RewardType.objects.get_or_create(slug=t['slug'], defaults={'name': t['name']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Created: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {obj.name}"))
