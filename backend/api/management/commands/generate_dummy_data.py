from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import (
    UserProfile, Portfolio, Investment, StockAlert,
    AIRecommendation, StockData, AIAnalysis
)
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta
import json

class Command(BaseCommand):
    help = 'Generate realistic dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to generate dummy data...')
        
        # Sample stock data
        STOCKS = [
            ('AAPL', 'Apple Inc.', 175.50, 180.00, 173.00, 1000000, 2800000000000),
            ('GOOGL', 'Alphabet Inc.', 142.75, 145.00, 141.00, 800000, 1800000000000),
            ('MSFT', 'Microsoft Corporation', 380.25, 385.00, 378.00, 900000, 2900000000000),
            ('AMZN', 'Amazon.com Inc.', 168.40, 170.00, 167.00, 750000, 1700000000000),
            ('TSLA', 'Tesla Inc.', 195.70, 198.00, 193.00, 1200000, 620000000000),
            ('META', 'Meta Platforms Inc.', 485.90, 490.00, 483.00, 600000, 1240000000000),
        ]

        # Real-looking user data
        USERS = [
            {
                'username': 'sarah.patel',
                'first_name': 'Sarah',
                'last_name': 'Patel',
                'email': 'sarah.patel@example.com',
                'profile': {
                    'risk_tolerance': 7,
                    'investment_horizon': 15
                }
            },
            {
                'username': 'michael.chen',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'michael.chen@example.com',
                'profile': {
                    'risk_tolerance': 5,
                    'investment_horizon': 10
                }
            },
            {
                'username': 'emma.wilson',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'email': 'emma.wilson@example.com',
                'profile': {
                    'risk_tolerance': 8,
                    'investment_horizon': 20
                }
            },
            {
                'username': 'raj.kumar',
                'first_name': 'Raj',
                'last_name': 'Kumar',
                'email': 'raj.kumar@example.com',
                'profile': {
                    'risk_tolerance': 6,
                    'investment_horizon': 12
                }
            },
            {
                'username': 'alex.rodriguez',
                'first_name': 'Alex',
                'last_name': 'Rodriguez',
                'email': 'alex.rodriguez@example.com',
                'profile': {
                    'risk_tolerance': 9,
                    'investment_horizon': 25
                }
            }
        ]

        # Create test users and profiles
        for user_data in USERS:
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='testpass123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                UserProfile.objects.create(
                    user=user,
                    risk_tolerance=user_data['profile']['risk_tolerance'],
                    investment_horizon=user_data['profile']['investment_horizon']
                )
                self.stdout.write(f'Created user and profile for {user_data["first_name"]} {user_data["last_name"]}')
            except Exception as e:
                self.stdout.write(f'User {user_data["username"]} already exists')
                user = User.objects.get(username=user_data['username'])

            # Create stock data
            for symbol, name, price, high, low, volume, market_cap in STOCKS:
                # Add some randomization to prices
                current_price = Decimal(str(price + random.uniform(-5, 5)))
                StockData.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        'name': name,
                        'current_price': current_price,
                        'daily_high': Decimal(str(high + random.uniform(-2, 2))),
                        'daily_low': Decimal(str(low + random.uniform(-2, 2))),
                        'volume': volume + random.randint(-100000, 100000),
                        'market_cap': market_cap,
                        'pe_ratio': Decimal(str(random.uniform(15, 30))),
                        'dividend_yield': Decimal(str(random.uniform(0, 3))),
                    }
                )

            # Create personalized portfolios based on user profile
            portfolio_types = {
                'Conservative': 'Focus on stable, dividend-paying stocks with lower risk',
                'Aggressive Growth': 'High-growth technology and emerging market stocks',
                'Balanced': 'Mix of growth and value stocks for steady returns',
                'Technology Focus': 'Concentrated in leading tech companies'
            }

            for p_name, p_desc in portfolio_types.items():
                portfolio = Portfolio.objects.create(
                    user=user,
                    name=f"{user_data['first_name']}'s {p_name} Portfolio",
                    description=p_desc
                )

                # Create investments for each portfolio
                for _ in range(random.randint(2, 4)):
                    stock = random.choice(STOCKS)
                    Investment.objects.create(
                        portfolio=portfolio,
                        symbol=stock[0],
                        shares=Decimal(str(random.randint(10, 100))),
                        entry_price=Decimal(str(stock[2] + random.uniform(-10, 10))),
                        entry_date=timezone.now() - timedelta(days=random.randint(1, 365)),
                        notes=f"Strategic investment in {stock[1]} aligned with {p_name} strategy"
                    )

            # Create stock alerts
            for _ in range(random.randint(2, 4)):
                stock = random.choice(STOCKS)
                alert_type = random.choice(['ABOVE', 'BELOW'])
                base_price = stock[2]
                threshold = base_price * (1.1 if alert_type == 'ABOVE' else 0.9)
                
                StockAlert.objects.create(
                    user=user,
                    symbol=stock[0],
                    alert_type=alert_type,
                    price_threshold=Decimal(str(threshold)),
                    is_active=True
                )

            # Create AI recommendations
            for _ in range(random.randint(2, 4)):
                stock = random.choice(STOCKS)
                sentiment = random.choice(['Bullish', 'Bearish', 'Neutral'])
                confidence = random.uniform(60, 95)
                
                analysis_data = {
                    'technical_indicators': {
                        'moving_average': random.choice(['Above', 'Below', 'At']),
                        'rsi': random.randint(30, 70),
                        'macd': random.choice(['Positive', 'Negative']),
                    },
                    'market_sentiment': sentiment,
                    'risk_level': random.choice(['Low', 'Medium', 'High']),
                }
                
                AIRecommendation.objects.create(
                    user=user,
                    symbol=stock[0],
                    recommendation=f"{sentiment} outlook based on technical analysis and market sentiment",
                    confidence_score=Decimal(str(confidence)),
                    analysis_data=analysis_data
                )

            # Create AI analyses with more personalized queries
            providers = ['GEMINI', 'GPT', 'CLAUDE']
            queries = [
                f'Analyze potential risks in {user_data["first_name"]}\'s technology portfolio',
                f'Evaluate dividend stocks suitable for {user_data["first_name"]}\'s investment horizon of {user_data["profile"]["investment_horizon"]} years',
                f'Suggest portfolio adjustments based on {user_data["first_name"]}\'s risk tolerance of {user_data["profile"]["risk_tolerance"]}/10'
            ]
            
            for _ in range(random.randint(2, 4)):
                AIAnalysis.objects.create(
                    user=user,
                    query=random.choice(queries),
                    provider=random.choice(providers),
                    response=f"Detailed analysis tailored to {user_data['first_name']}'s investment profile...",
                    summary=f"Key recommendations for {user_data['first_name']}'s portfolio strategy..."
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data'))
