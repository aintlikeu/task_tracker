import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestJwtAuthentication:
    def test_get_jwt_token_valid_data(self, client, user):
        url = reverse('token_obtain_pair')
        # it's necessary to specify the password explicitly, because it's hashed in the database
        password = 'password_1'
        valid_data = {'username': user.username, 'password': password}
        response = client.post(url, data=valid_data)
        assert response.status_code == 200
        assert 'refresh' in response.data
        assert 'access' in response.data

    def test_get_jwt_token_invalid_data(self, client, user):
        url = reverse('token_obtain_pair')
        password = 'incorrect_password'
        valid_data = {'username': user.username, 'password': password}
        response = client.post(url, data=valid_data)
        assert response.status_code == 401
        assert 'refresh' not in response.data
        assert 'access' not in response.data

    def test_refresh_jwt_token(self, client, user, jwt_tokens):
        url = reverse('token_refresh')
        valid_data = {'refresh': jwt_tokens['refresh']}
        response = client.post(url, data=valid_data)
        assert response.status_code == 200
        assert 'access' in response.data

    def test_verify_jwt_valid_token(self, client, user, jwt_tokens):
        url = reverse('token_verify')
        valid_data = {'token': jwt_tokens['access']}
        response = client.post(url, data=valid_data)
        assert response.status_code == 200

    def test_verify_jwt_invalid_token(self, client, user, jwt_tokens):
        url = reverse('token_verify')
        valid_data = {'token': 'invalid_token'}
        response = client.post(url, data=valid_data)
        assert response.status_code == 401
