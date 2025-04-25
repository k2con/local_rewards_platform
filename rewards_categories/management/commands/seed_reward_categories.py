from django.core.management.base import BaseCommand
from rewards_categories.models import RewardCategory
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed initial reward categories into the database'

    def handle(self, *args, **kwargs):
        categories = [
            'Technology',
            'Gastronomy',
            'Supermarkets',
            'Pharmacy',
            'Gas stations',
            'Gift Card Vendors',
            'Credit for cellphone',
            'Clothing Stores',
            'Fitness and Lifestyle',
            'Restaurants',
            'Hotels & Malls',
            'Hotels',
            'Hardware / Home Decor Stores',
            'Activities',
            'Stores',
            'Spas / Wellness',
            'Perfumery Stores',
            'Hardware / Office Supplies',
            'Electronic Stores',
            'Delivery',
            'Book Stores',
            'Sun Glasses Boutique',
            'Liquor/ Wine Stores',
            'Duty Free - Jewelry / Perfume',
            'Cellphone',
            'Beach Clubs',
            'Toy Stores',
            'Telephone Services',
            'Movie Theatres',
            'Flowershop',
            'Drugstore',
            'Courier',
            'Car Wash',
            'Candy Shop',
            'Other',
        ]

        for name in categories:
            slug = slugify(name)
            obj, created = RewardCategory.objects.get_or_create(slug=slug, defaults={'name': name})
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Created: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {name}"))
