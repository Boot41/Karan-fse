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
    INVESTMENT_STYLE_CHOICES = [
        ('Conservative', 'Conservative'),
        ('Moderate', 'Moderate'),
        ('Aggressive', 'Aggressive'),
    ]

    INVESTMENT_GOAL_CHOICES = [
        ('Retirement', 'Retirement'),
        ('Wealth Building', 'Wealth Building'),
        ('Short Term', 'Short Term Gains'),
        ('Regular Income', 'Regular Income'),
    ]

    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ]

    INCOME_RANGE_CHOICES = [
        ('0-5', '0-5 LPA'),
        ('5-10', '5-10 LPA'),
        ('10-20', '10-20 LPA'),
        ('20+', '20+ LPA'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    risk_tolerance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    investment_style = models.CharField(
        max_length=20,
        choices=INVESTMENT_STYLE_CHOICES,
        default='Moderate'
    )
    income_range = models.CharField(
        max_length=10,
        choices=INCOME_RANGE_CHOICES,
        blank=True
    )
    investment_goal = models.CharField(
        max_length=20,
        choices=INVESTMENT_GOAL_CHOICES,
        blank=True
    )
    investment_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='Beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
