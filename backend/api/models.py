from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    """
    Stores additional user details for investment advisory.
    This data is collected after successful registration.
    """
    
    INVESTMENT_TYPE_CHOICES = [
        ('SHORT_TERM', 'Short Term'),
        ('MID_TERM', 'Mid Term'),
        ('LONG_TERM', 'Long Term')
    ]
    
    INVESTMENT_REASON_CHOICES = [
        ('WEALTH_GROWTH', 'Wealth Growth'),
        ('EDUCATION', 'Education'),
        ('RETIREMENT', 'Retirement'),
        ('ESTATE', 'Estate Planning')
    ]
    
    INCOME_RANGE_CHOICES = [
        ('UNDER_2_LPA', 'Under 2 LPA'),
        ('2_TO_5_LPA', '2-5 LPA'),
        ('5_TO_10_LPA', '5-10 LPA'),
        ('10_TO_20_LPA', '10-20 LPA'),
        ('20_LPA_PLUS', '20 LPA+')
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced')
    ]
    
    RISK_TOLERANCE_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    PREFERRED_SECTORS_CHOICES = [
        ('EDUCATION', 'Education'),
        ('REAL_ESTATE', 'Real Estate'),
        ('WEALTH_GROWTH', 'Wealth Growth'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the main User model
    name = models.CharField(max_length=100)  # User's display name/profile name
    risk_tolerance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=5)  # Integer range from 0-10 with default 5
    investment_type = models.CharField(max_length=15, choices=INVESTMENT_TYPE_CHOICES, default='LONG_TERM')
    investment_reason = models.CharField(max_length=20, choices=INVESTMENT_REASON_CHOICES, default='WEALTH_GROWTH')
    income_range = models.CharField(max_length=20, choices=INCOME_RANGE_CHOICES, default='UNDER_2_LPA')  # Default set here
    investment_experience = models.CharField(max_length=15, choices=EXPERIENCE_LEVEL_CHOICES, default='BEGINNER')  # Default set to BEGINNER
    investment_style = models.CharField(max_length=50, choices=[
        ('Conservative', 'Conservative'),
        ('Balanced Growth', 'Balanced Growth'),
        ('Aggressive Growth', 'Aggressive Growth'),
    ], default='Conservative')
    experience_level = models.CharField(max_length=15, choices=EXPERIENCE_LEVEL_CHOICES, default='BEGINNER')
    investment_horizon = models.IntegerField(default=1)  # Assuming this is in years
    
    # Correctly defined preferred_sectors as a CharField with choices
    preferred_sectors = models.CharField(
        max_length=20,  # Ensure this matches the length of your options
        choices=PREFERRED_SECTORS_CHOICES,
        default='EDUCATION'  # Set a default value if needed
    )
    
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for profile creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for profile updates

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Portfolio(models.Model):
    """
    Stores a user's stock portfolio details.
    This includes the stocks they have purchased, their quantity, and purchase details.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')  # Linking to the User model
    stock_symbol = models.CharField(max_length=10, db_index=True)  # Ticker symbol (e.g., AAPL, TSLA)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per share at purchase
    quantity = models.IntegerField()  # Number of shares bought
    purchase_date = models.DateTimeField(auto_now_add=True)  # Date when the stock was purchased
    last_updated = models.DateTimeField(auto_now=True)  # Last modified timestamp
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Current value of holdings
    notes = models.TextField(blank=True)  # Optional notes on the investment

    class Meta:
        unique_together = ['user', 'stock_symbol']  # Ensures a user can't have duplicate stock entries
        indexes = [
            models.Index(fields=['user', 'stock_symbol']),
            models.Index(fields=['stock_symbol', '-purchase_date'])
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.stock_symbol} holdings"


class MarketData(models.Model):
    """
    Stores real-time market data.
    This data includes stock prices, daily changes, and sentiment analysis.
    """
    symbol = models.CharField(max_length=10, db_index=True)  # Stock symbol (e.g., AAPL)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # Current stock price
    daily_change = models.DecimalField(max_digits=10, decimal_places=2)  # Daily price change
    volume = models.BigIntegerField()  # Stock volume for the day
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Sentiment score
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the market data was collected

    def __str__(self):
        return f"Market Data for {self.symbol} at {self.timestamp}"
