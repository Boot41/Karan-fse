from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_user, login_user, logout_user, forgot_password, stock_advisory_view,
    UserProfileViewSet, PortfolioViewSet, MarketDataViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.http import JsonResponse

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'market', MarketDataViewSet, basename='market')

# URL patterns
urlpatterns = [
    # Home view
    path('', lambda request: JsonResponse({"message": "Welcome to the API!"}), name='home'),

    # Register all ViewSet endpoints
    path('api/', include(router.urls)),  # Automatically include the ViewSet routes

    # Authentication endpoints
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/login/', login_user, name='login'),
    path('api/auth/logout/', logout_user, name='logout'),
    path('api/auth/forgot-password/', forgot_password, name='forgot_password'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Portfolio summary endpoint (calls PortfolioViewSet summary action)
    path('api/portfolio/summary/', PortfolioViewSet.as_view({'get': 'summary'}), name='portfolio-summary'),

    # Market data endpoints
    path('api/market/live/<str:symbol>/', MarketDataViewSet.as_view({'get': 'fetch_live_data'}), name='market-live-data'),
    path('api/market/recommendations/', MarketDataViewSet.as_view({'get': 'get_recommendations'}), name='market-recommendations'),

    # Stock advisory endpoint
    path('api/stock/advisory/', stock_advisory_view, name='stock-advisory'),

    # Redundant endpoints using stock_advisory_view (if needed)
    path('api/stock/price/', stock_advisory_view, name='stock-price'),
    path('api/stock-price-alpha-vantage/', stock_advisory_view, name='stock_price_alpha_vantage'),
    path('api/stock-price-finhub/', stock_advisory_view, name='stock_price_finhub'),
]