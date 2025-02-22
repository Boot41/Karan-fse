from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    INVESTMENT_STYLES = [
        ('short-term', 'Short Term'),
        ('long-term', 'Long Term'),
        ('day-trading', 'Day Trading'),
        ('value-investing', 'Value Investing')
    ]

    INCOME_RANGES = [
        ('Less than 2 LPA', 'Less than ₹2 LPA'),
        ('2-5 LPA', '₹2 - ₹5 LPA'),
        ('5-10 LPA', '₹5 - ₹10 LPA'),
        ('10-20 LPA', '₹10 - ₹20 LPA'),
        ('More than 20 LPA', 'More than ₹20 LPA')
    ]

    INVESTMENT_GOALS = [
        ('financial-growth', 'Financial Growth'),
        ('education', 'Education'),
        ('retirement', 'Retirement'),
        ('real-estate', 'Real Estate')
    ]

    INVESTMENT_EXPERIENCE = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    risk_tolerance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Risk tolerance scale: 1 (Low) to 10 (High)"
    )
    investment_style = models.CharField(
        max_length=20,
        choices=INVESTMENT_STYLES,
        default='short-term'
    )
    income_range = models.CharField(
        max_length=20,
        choices=INCOME_RANGES,
        default='2-5 LPA'
    )
    investment_goal = models.CharField(
        max_length=20,
        choices=INVESTMENT_GOALS,
        default='financial-growth'
    )
    investment_experience = models.CharField(
        max_length=20,
        choices=INVESTMENT_EXPERIENCE,
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s Profile"
