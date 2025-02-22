from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import UserProfile
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        # Sample data
        users_data = [
            {
                'email': 'rahul.sharma@gmail.com',
                'username': 'rahul_sharma',
                'password': 'testpass123',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
                'profile': {
                    'full_name': 'Rahul Sharma',
                    'risk_tolerance': 8,
                    'investment_style': 'day-trading',
                    'income_range': '10-20 LPA',
                    'investment_goal': 'financial-growth',
                    'investment_experience': 'advanced'
                }
            },
            {
                'email': 'priya.patel@gmail.com',
                'username': 'priya_patel',
                'password': 'testpass123',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'profile': {
                    'full_name': 'Priya Patel',
                    'risk_tolerance': 4,
                    'investment_style': 'value-investing',
                    'income_range': '5-10 LPA',
                    'investment_goal': 'education',
                    'investment_experience': 'intermediate'
                }
            },
            {
                'email': 'amit.kumar@gmail.com',
                'username': 'amit_kumar',
                'password': 'testpass123',
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'profile': {
                    'full_name': 'Amit Kumar',
                    'risk_tolerance': 6,
                    'investment_style': 'long-term',
                    'income_range': '2-5 LPA',
                    'investment_goal': 'retirement',
                    'investment_experience': 'beginner'
                }
            },
            {
                'email': 'neha.gupta@gmail.com',
                'username': 'neha_gupta',
                'password': 'testpass123',
                'first_name': 'Neha',
                'last_name': 'Gupta',
                'profile': {
                    'full_name': 'Neha Gupta',
                    'risk_tolerance': 7,
                    'investment_style': 'short-term',
                    'income_range': 'More than 20 LPA',
                    'investment_goal': 'real-estate',
                    'investment_experience': 'expert'
                }
            },
            {
                'email': 'vikram.singh@gmail.com',
                'username': 'vikram_singh',
                'password': 'testpass123',
                'first_name': 'Vikram',
                'last_name': 'Singh',
                'profile': {
                    'full_name': 'Vikram Singh',
                    'risk_tolerance': 9,
                    'investment_style': 'day-trading',
                    'income_range': '10-20 LPA',
                    'investment_goal': 'financial-growth',
                    'investment_experience': 'advanced'
                }
            }
        ]

        self.stdout.write('Creating users and profiles...')

        for user_data in users_data:
            profile_data = user_data.pop('profile')
            
            # Create user
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.email}')
            
            # Create or update profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults=profile_data
            )
            
            if created:
                self.stdout.write(f'Created profile for: {user.email}')
            
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
