from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import UserProfile
from django.contrib.auth.hashers import make_password

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy users for testing'

    def handle(self, *args, **kwargs):
        # Dummy users data
        users_data = [
    {
        'email': 'michael.brown@gmail.com',
        'username': 'michael.brown',
        'password': 'mike123',
        'profile': {
            'risk_tolerance': 3,
            'investment_style': 'Conservative',
            'experience_level': 'BEGINNER',
            'investment_horizon': 2,
            'preferred_sectors': ['Technology', 'Healthcare'],
            'income_range': 'UNDER_2_LPA'
        }
    },
    {
        'email': 'sophia.williams@gmail.com',
        'username': 'sophia.williams',
        'password': 'sophia123',
        'profile': {
            'risk_tolerance': 6,
            'investment_style': 'Balanced Growth',
            'experience_level': 'INTERMEDIATE',
            'investment_horizon': 4,
            'preferred_sectors': ['Real Estate', 'Energy'],
            'income_range': '2_TO_5_LPA'
        }
    },
    {
        'email': 'david.johnson@gmail.com',
        'username': 'david.johnson',
        'password': 'david123',
        'profile': {
            'risk_tolerance': 8,
            'investment_style': 'Aggressive Growth',
            'experience_level': 'EXPERT',
            'investment_horizon': 5,
            'preferred_sectors': ['Finance', 'Retail'],
            'income_range': '5_TO_10_LPA'
        }
    },
    {
        'email': 'linda.martinez@gmail.com',
        'username': 'linda.martinez',
        'password': 'linda123',
        'profile': {
            'risk_tolerance': 4,
            'investment_style': 'Growth',
            'experience_level': 'BEGINNER',
            'investment_horizon': 3,
            'preferred_sectors': ['Healthcare', 'Technology'],
            'income_range': '10_TO_20_LPA'
        }
    },
    {
        'email': 'james.lee@gmail.com',
        'username': 'james.lee',
        'password': 'james123',
        'profile': {
            'risk_tolerance': 5,
            'investment_style': 'Conservative',
            'experience_level': 'INTERMEDIATE',
            'investment_horizon': 6,
            'preferred_sectors': ['Agriculture', 'Energy'],
            'income_range': '20_LPA_PLUS'
        }
    },
    {
        'email': 'emily.davis@gmail.com',
        'username': 'emily.davis',
        'password': 'emily123',
        'profile': {
            'risk_tolerance': 2,
            'investment_style': 'Balanced Growth',
            'experience_level': 'BEGINNER',
            'investment_horizon': 4,
            'preferred_sectors': ['Technology', 'Finance'],
            'income_range': 'UNDER_2_LPA'
        }
    },
    {
        'email': 'william.garcia@gmail.com',
        'username': 'william.garcia',
        'password': 'will123',
        'profile': {
            'risk_tolerance': 7,
            'investment_style': 'Growth',
            'experience_level': 'INTERMEDIATE',
            'investment_horizon': 5,
            'preferred_sectors': ['Healthcare', 'Retail'],
            'income_range': '2_TO_5_LPA'
        }
    },
    {
        'email': 'olivia.miller@gmail.com',
        'username': 'olivia.miller',
        'password': 'olivia123',
        'profile': {
            'risk_tolerance': 9,
            'investment_style': 'Aggressive Growth',
            'experience_level': 'EXPERT',
            'investment_horizon': 8,
            'preferred_sectors': ['Energy', 'Agriculture'],
            'income_range': '5_TO_10_LPA'
        }
    }
]
        # Create users and profiles
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'password': make_password(user_data['password'])
                }
            )

            if created:
                profile_data = user_data['profile']
                UserProfile.objects.create(
                    user=user,
                    risk_tolerance=profile_data['risk_tolerance'],
                    investment_style=profile_data['investment_style'],
                    experience_level=profile_data['experience_level'],
                    investment_horizon=profile_data['investment_horizon'],
                    preferred_sectors=profile_data['preferred_sectors']
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {user.email}'))