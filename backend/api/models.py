from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_tolerance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Risk tolerance level from 1 (low) to 10 (high)"
    )
    investment_goal = models.CharField(max_length=100)
    preferred_investment_duration = models.IntegerField(
        help_text="Preferred investment duration in months"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_high = models.DecimalField(max_digits=10, decimal_places=2)
    daily_low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    market_cap = models.BigIntegerField()
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    last_updated = models.DateTimeField(auto_now=True)

class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    recommendation_type = models.CharField(max_length=20)  # buy, sell, hold
    confidence_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

class StockAlert(models.Model):
    ALERT_TYPES = (
        ('price_above', 'Price Above'),
        ('price_below', 'Price Below'),
        ('percent_change', 'Percent Change'),
        ('volume_above', 'Volume Above'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    notification_email = models.EmailField()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'stock_symbol', 'is_active']),
        ]

    def __str__(self):
        return f"{self.stock_symbol} - {self.alert_type} - {self.target_value}"
