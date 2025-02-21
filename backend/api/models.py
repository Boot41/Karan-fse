from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class AIAnalysis(models.Model):
    """Model for storing AI analysis results from different LLM providers"""
    PROVIDER_CHOICES = [
        ('GEMINI', 'Google Gemini'),
        ('GPT', 'OpenAI GPT'),
        ('CLAUDE', 'Anthropic Claude')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    response = models.TextField()
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'provider']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.provider} Analysis for {self.user.username}"

class UserProfile(models.Model):
    """Extended user profile with investment preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_tolerance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Risk tolerance scale: 1 (Low) to 10 (High)"
    )
    investment_horizon = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Investment horizon in years"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Portfolio(models.Model):
    """User's investment portfolio"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name} Portfolio"

class Investment(models.Model):
    """Individual stock investments in a portfolio"""
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.portfolio.name} - {self.symbol}"

class StockAlert(models.Model):
    """Price alerts for stocks"""
    ALERT_TYPES = [
        ('ABOVE', 'Price Above'),
        ('BELOW', 'Price Below'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    alert_type = models.CharField(max_length=5, choices=ALERT_TYPES)
    price_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} {self.alert_type} {self.price_threshold}"

class AIRecommendation(models.Model):
    """AI-generated investment recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    recommendation = models.TextField()
    confidence_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    analysis_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} Analysis for {self.user.username}"

class StockData(models.Model):
    """Cache for frequently accessed stock data"""
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_high = models.DecimalField(max_digits=10, decimal_places=2)
    daily_low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    market_cap = models.BigIntegerField()
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"
