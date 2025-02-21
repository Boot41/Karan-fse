import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }

@pytest.fixture
def created_user(user_data):
    user = User.objects.create_user(
        username=user_data['email'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    return user

@pytest.mark.django_db
class TestAuthentication:
    def test_user_registration(self, api_client, user_data):
        url = reverse('rest_register')
        response = api_client.post(url, user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'key' in response.data

    def test_user_login(self, api_client, user_data, created_user):
        url = reverse('rest_login')
        data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_invalid_login(self, api_client):
        url = reverse('rest_login')
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self, api_client, user_data, created_user):
        # First login to get tokens
        login_url = reverse('rest_login')
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        login_response = api_client.post(login_url, login_data)
        refresh_token = login_response.data['refresh']

        # Try to refresh token
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = api_client.post(refresh_url, refresh_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_password_change(self, api_client, user_data, created_user):
        # Login first
        api_client.force_authenticate(user=created_user)
        url = reverse('rest_password_change')
        data = {
            'old_password': user_data['password'],
            'new_password1': 'NewTestPass123!',
            'new_password2': 'NewTestPass123!'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

        # Try logging in with new password
        login_url = reverse('rest_login')
        login_data = {
            'email': user_data['email'],
            'password': 'NewTestPass123!'
        }
        response = api_client.post(login_url, login_data)
        assert response.status_code == status.HTTP_200_OK
