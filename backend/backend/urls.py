"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    UserProfileViewSet, PortfolioViewSet,
    InvestmentViewSet, StockAlertViewSet,
    AIRecommendationViewSet, AIAnalysisViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'investments', InvestmentViewSet, basename='investment')
router.register(r'stock-alerts', StockAlertViewSet, basename='stock-alert')
router.register(r'ai-recommendations', AIRecommendationViewSet, basename='ai-recommendation')
router.register(r'ai-analysis', AIAnalysisViewSet, basename='ai-analysis')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)