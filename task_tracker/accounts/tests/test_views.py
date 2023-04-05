import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from accounts.models import CustomUser


@pytest.mark.django_db
class TestCustomUserViewSetAnonymous:
    """
    Test class for unauthenticated endpoints of the CustomUserViewSet.
    """
    def test_user_creation_valid_data(self, client):
        url = reverse('users-list')
        valid_data = {'username': 'test', 'password': 'password!1'}
        response = client.post(url, data=valid_data)
        assert response.status_code == 201
        assert response.data['id'] == 1
        assert response.data['username'] == valid_data['username']
        assert CustomUser.objects.count() == 1
        assert CustomUser.objects.get(pk=1).username == valid_data['username']

    def test_user_creation_invalid_data(self, client):
        url = reverse('users-list')
        valid_data = {'username': 'test', 'password': '1'}
        response = client.post(url, data=valid_data)
        assert type(response.data['message']) == ValidationError
        assert response.status_code == 400
        assert CustomUser.objects.count() == 0

    def test_get_user_list_as_anonymous(self, client, user):
        url = reverse('users-list')
        response = client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestCustomUserViewSetStandardAuth:
    """
    Test class for endpoints of the CustomUserViewSet when accessed with standard authentication.
    """
    def test_get_user_list_as_authenticated(self, authenticated_client, user):
        url = reverse('users-list')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.data[0]['id'] == 1
        assert response.data[0]['username'] == user.username

    def test_user_delete_by_owner(self, authenticated_client, user):
        assert CustomUser.objects.count() == 1
        url = reverse('users-detail', kwargs={'pk': user.id})
        response = authenticated_client.delete(url)
        assert response.status_code == 204
        assert CustomUser.objects.count() == 0

    def test_user_delete_by_admin(self, authenticated_admin_client, user):
        assert CustomUser.objects.count() == 2
        url = reverse('users-detail', kwargs={'pk': user.id})
        response = authenticated_admin_client.delete(url)
        assert response.status_code == 204
        assert CustomUser.objects.count() == 1

    def test_user_delete_by_another_user(self, authenticated_client, user2):
        assert CustomUser.objects.count() == 2
        url = reverse('users-detail', kwargs={'pk': user2.id})
        response = authenticated_client.delete(url)
        assert response.status_code == 403
        assert CustomUser.objects.count() == 2

    def test_change_password_valid_data(self, authenticated_admin_client):
        url = reverse('users-change-password')
        old_pass_hash = CustomUser.objects.get(pk=1).password
        valid_data = {'password': 'password_10'}
        response = authenticated_admin_client.post(url, data=valid_data)
        assert response.status_code == 204
        new_pass_hash = CustomUser.objects.get(pk=1).password
        assert old_pass_hash != new_pass_hash

    def test_change_password_invalid_data(self, authenticated_admin_client):
        url = reverse('users-change-password')
        old_pass_hash = CustomUser.objects.get(pk=1).password
        valid_data = {'password': '1'}
        response = authenticated_admin_client.post(url, data=valid_data)
        assert response.status_code == 400
        new_pass_hash = CustomUser.objects.get(pk=1).password
        assert old_pass_hash == new_pass_hash


@pytest.mark.django_db
class TestCustomUserViewSetJwtAuth:
    """
    Test class for endpoints of the CustomUserViewSet when accessed with JWT token
    """
    def test_get_user_list_as_authenticated_jwt(self, authenticated_api_client):
        url = reverse('users-list')
        response = authenticated_api_client.get(url)
        assert response.status_code == 200

    def test_user_delete_by_owner_jwt(self, authenticated_api_client):
        assert CustomUser.objects.count() == 1
        url = reverse('users-detail', kwargs={'pk': 1})
        response = authenticated_api_client.delete(url)
        assert response.status_code == 204
        assert CustomUser.objects.count() == 0

    def test_user_delete_by_admin_jwt(self, authenticated_admin_api_client, user):
        assert CustomUser.objects.count() == 2
        url = reverse('users-detail', kwargs={'pk': user.id})
        response = authenticated_admin_api_client.delete(url)
        assert response.status_code == 204
        assert CustomUser.objects.count() == 1

    def test_user_delete_by_another_user_jwt(self, authenticated_api_client, user2):
        assert CustomUser.objects.count() == 2
        url = reverse('users-detail', kwargs={'pk': user2.id})
        response = authenticated_api_client.delete(url)
        assert response.status_code == 403
        assert CustomUser.objects.count() == 2

    def test_change_password_valid_data_jwt(self, authenticated_api_client):
        url = reverse('users-change-password')
        old_pass_hash = CustomUser.objects.get(pk=1).password
        valid_data = {'password': 'password_10'}
        response = authenticated_api_client.post(url, data=valid_data)
        assert response.status_code == 204
        new_pass_hash = CustomUser.objects.get(pk=1).password
        assert old_pass_hash != new_pass_hash

    def test_change_password_invalid_data_jwt(self, authenticated_api_client):
        url = reverse('users-change-password')
        old_pass_hash = CustomUser.objects.get(pk=1).password
        valid_data = {'password': '1'}
        response = authenticated_api_client.post(url, data=valid_data)
        assert response.status_code == 400
        new_pass_hash = CustomUser.objects.get(pk=1).password
        assert old_pass_hash == new_pass_hash
