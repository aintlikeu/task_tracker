import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from manager.models import Task


# clients
@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def authenticated_admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


# users
@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='test_1', password='password_1')


@pytest.fixture
def user2():
    return CustomUser.objects.create_user(username='test_2', password='password_2')


@pytest.fixture
def admin_user():
    return CustomUser.objects.create_superuser(username='admin', password='password_1')


# tasks
@pytest.fixture
def task(user, user2):
    task = Task.objects.create(
        name='Test task',
        description='Test description',
        owner=user,
        assigned_to=user2,
        completed=False
    )
    return task


# jwt tokens
@pytest.fixture
def jwt_tokens(client, user):
    url = reverse('token_obtain_pair')
    password = 'password_1'
    valid_data = {'username': user.username, 'password': password}
    response = client.post(url, data=valid_data)
    return response.data


# clients for tests that use JWT authentication
@pytest.fixture
def authenticated_api_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def authenticated_admin_api_client(admin_user):
    client = APIClient()
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
