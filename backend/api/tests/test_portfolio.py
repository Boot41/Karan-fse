import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import Portfolio, Investment
from decimal import Decimal

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def portfolio_data():
    return {
        'name': 'Test Portfolio',
        'description': 'A test portfolio'
    }

@pytest.fixture
def created_portfolio(user, portfolio_data):
    return Portfolio.objects.create(
        user=user,
        name=portfolio_data['name'],
        description=portfolio_data['description']
    )

@pytest.fixture
def investment_data():
    return {
        'stock_symbol': 'AAPL',
        'shares': 10,
        'purchase_price': '150.00'
    }

@pytest.mark.django_db
class TestPortfolioManagement:
    def test_create_portfolio(self, authenticated_client, portfolio_data):
        url = reverse('api:portfolio-list')
        response = authenticated_client.post(url, portfolio_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == portfolio_data['name']
        assert response.data['description'] == portfolio_data['description']

    def test_list_portfolios(self, authenticated_client, created_portfolio):
        url = reverse('api:portfolio-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == created_portfolio.name

    def test_retrieve_portfolio(self, authenticated_client, created_portfolio):
        url = reverse('api:portfolio-detail', kwargs={'pk': created_portfolio.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == created_portfolio.name

    def test_update_portfolio(self, authenticated_client, created_portfolio):
        url = reverse('api:portfolio-detail', kwargs={'pk': created_portfolio.id})
        updated_data = {
            'name': 'Updated Portfolio',
            'description': 'Updated description'
        }
        response = authenticated_client.put(url, updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == updated_data['name']

    def test_delete_portfolio(self, authenticated_client, created_portfolio):
        url = reverse('api:portfolio-detail', kwargs={'pk': created_portfolio.id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Portfolio.objects.count() == 0

    def test_add_investment(self, authenticated_client, created_portfolio, investment_data):
        url = reverse('api:investment-list')
        data = {**investment_data, 'portfolio': created_portfolio.id}
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['stock_symbol'] == investment_data['stock_symbol']
        assert Decimal(response.data['shares']) == Decimal(investment_data['shares'])

    def test_unauthorized_access(self, api_client, portfolio_data):
        url = reverse('api:portfolio-list')
        response = api_client.post(url, portfolio_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_portfolio_total_value(self, authenticated_client, created_portfolio):
        # Create multiple investments
        Investment.objects.create(
            portfolio=created_portfolio,
            stock_symbol='AAPL',
            shares=10,
            purchase_price=Decimal('150.00')
        )
        Investment.objects.create(
            portfolio=created_portfolio,
            stock_symbol='GOOGL',
            shares=5,
            purchase_price=Decimal('2500.00')
        )

        url = reverse('api:portfolio-detail', kwargs={'pk': created_portfolio.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'total_value' in response.data
        assert isinstance(response.data['total_value'], str)  # Should be decimal string
        assert Decimal(response.data['total_value']) > 0
