from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal

class UserProfile(models.Model):
    RISK_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MODERATE', 'Moderate Risk'),
        ('HIGH', 'High Risk')
    ]
    
    EXPERIENCE_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('EXPERT', 'Expert')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, default='MODERATE')
    investment_style = models.CharField(max_length=100, default='Growth')
    experience_level = models.CharField(max_length=15, choices=EXPERIENCE_CHOICES, default='BEGINNER')
    investment_horizon = models.IntegerField(default=5)  # in years
    preferred_sectors = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['risk_tolerance', 'investment_style']),
            models.Index(fields=['experience_level', 'investment_horizon'])
        ]

    def __str__(self):
        return f"{self.user.email}'s Profile"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    stock_symbol = models.CharField(max_length=10, db_index=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'stock_symbol']
        indexes = [
            models.Index(fields=['user', 'stock_symbol']),
            models.Index(fields=['stock_symbol', '-purchase_date'])
        ]

    def __str__(self):
        return f"{self.user.email}'s {self.stock_symbol} holdings"

class MarketData(models.Model):
    symbol = models.CharField(max_length=10, unique=True, default='UNKNOWN', db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    daily_change = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    volume = models.BigIntegerField(default=0)
    high_52_week = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    low_52_week = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # -1 to 1

    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['symbol', '-timestamp']),
        ]
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.symbol} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
