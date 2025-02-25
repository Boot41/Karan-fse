from django.urls import path
from .views import (
    register_user,
    login_user,
    save_profile_view,
    UserProfileViewSet,
)

urlpatterns = [
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('profile/save/', save_profile_view, name='profile-save'),  # Ensure this is correctly defined
    # Add any other endpoints as needed
]
