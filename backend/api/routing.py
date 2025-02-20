from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/stock/(?P<symbol>\w+)/$', consumers.StockConsumer.as_asgi()),
    re_path(r'ws/portfolio/(?P<portfolio_id>\w+)/$', consumers.PortfolioConsumer.as_asgi()),
]
