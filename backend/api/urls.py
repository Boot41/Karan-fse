from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import permissions
from .views import (
    MarketDataViewSet,
    PortfolioViewSet,
    InvestmentViewSet,
    AIRecommendationViewSet,
    UserProfileViewSet
)

app_name = 'api'

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="AI Investment Platform API",
        default_version='v1',
        description="API documentation for AI Investment Platform",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'investments', InvestmentViewSet, basename='investment')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Stock market data endpoints
    path('market-data/get-stock-data/', 
         MarketDataViewSet.as_view({'get': 'get_stock_data'}),
         name='market-data-get-stock-data'),
         
    # AI recommendation endpoints
    path('recommendations/get-recommendation/',
         AIRecommendationViewSet.as_view({'post': 'get_recommendation'}),
         name='ai-recommendation-get-recommendation'),
]
