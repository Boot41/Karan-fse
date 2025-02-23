from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    register_user, login_user, forgot_password,
    logout_user, UserProfileViewSet, PortfolioViewSet, MarketDataViewSet,
    UserProfileView, UserProfileUpdateView, UserProfileSaveView
)

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'market', MarketDataViewSet, basename='market')

urlpatterns = [
    # Register all ViewSets
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/forgot-password/', forgot_password, name='forgot_password'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User Profile endpoints
    path('profile/', UserProfileView.as_view(), name='get-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/save/', UserProfileSaveView.as_view(), name='save-profile'),

    # Portfolio summary endpoint
    path('portfolio/summary/', PortfolioViewSet.as_view({'get': 'summary'}), name='portfolio-summary'),

    # Market data endpoints
    path('market/live/<str:symbol>/', MarketDataViewSet.as_view({'get': 'fetch_live_data'}), name='market-live-data'),
    path('market/recommendations/', MarketDataViewSet.as_view({'get': 'get_recommendations'}), name='market-recommendations'),
]
