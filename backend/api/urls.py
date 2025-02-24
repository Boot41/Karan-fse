from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    register_user, login_user, logout_user, forgot_password, stock_advisory_view,
    UserProfileViewSet, PortfolioViewSet, MarketDataViewSet
)

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'market', MarketDataViewSet, basename='market')

urlpatterns = [
    # Register all ViewSet endpoints
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/forgot-password/', forgot_password, name='forgot_password'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Portfolio summary endpoint (calls PortfolioViewSet summary action)
    path('portfolio/summary/', PortfolioViewSet.as_view({'get': 'summary'}), name='portfolio-summary'),

    # Market data endpoints
    # Fetch live market data for a given stock symbol (e.g., /market/live/TSLA/)
    path('market/live/<str:symbol>/', MarketDataViewSet.as_view({'get': 'fetch_live_data'}), name='market-live-data'),
    # Get market recommendations based on user data
    path('market/recommendations/', MarketDataViewSet.as_view({'get': 'get_recommendations'}), name='market-recommendations'),

    # Stock advisory endpoint (dynamic stock search, live data, user profile & AI advice)
    path('stock/advisory/', stock_advisory_view, name='stock-advisory'),

    # Redundant endpoints using stock_advisory_view (if needed)
    path('stock/price/', stock_advisory_view, name='stock-price'),
    path('api/stock-price-alpha-vantage/', stock_advisory_view, name='stock_price_alpha_vantage'),
    path('api/stock-price-finhub/', stock_advisory_view, name='stock_price_finhub'),
]