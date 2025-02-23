from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import UserProfile
from django.contrib.auth.hashers import make_password

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy users for testing'

    def handle(self, *args, **kwargs):
        # Create first dummy user
        user1, created = User.objects.get_or_create(
            email='john.doe123@gmail.com',
            defaults={
                'username': 'john.doe123',
                'password': make_password('john123')
            }
        )
        if created:
            UserProfile.objects.create(
                user=user1,
                risk_tolerance='MODERATE',
                investment_style='Growth',
                experience_level='INTERMEDIATE',
                investment_horizon=5,
                preferred_sectors=['Technology', 'Healthcare']
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user1.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User already exists: {user1.email}'))

        # Create second dummy user
        user2, created = User.objects.get_or_create(
            email='jane.doe123@gmail.com',
            defaults={
                'username': 'jane.doe123',
                'password': make_password('jane123')
            }
        )
        if created:
            UserProfile.objects.create(
                user=user2,
                risk_tolerance='HIGH',
                investment_style='Aggressive Growth',
                experience_level='EXPERT',
                investment_horizon=10,
                preferred_sectors=['Finance', 'Real Estate']
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user2.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User already exists: {user2.email}'))
