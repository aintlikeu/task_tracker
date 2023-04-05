import pytest
from django.urls import reverse
from manager.models import Task


@pytest.mark.django_db
class TestTaskViewSetAnonymous:
    """
    Test class for unauthenticated endpoints of the TaskViewSet.
    """
    def test_get_task_list_as_anonymous(self, client, task):
        url = reverse('tasks-list')
        response = client.get(url)
        assert response.status_code == 401

    def test_create_task_as_anonymous(self, client, user):
        url = reverse('tasks-list')
        valid_data = {
            'name': 'Test task',
            'description': 'Test description',
            'owner': user.username,
            'assigned_to': user.username,
            'completed': False
        }
        response = client.post(url, data=valid_data)
        assert response.status_code == 401


@pytest.mark.django_db
class TestTaskViewSetStandardAuth:
    """
    Test class for endpoints of the TaskViewSet when accessed with standard authentication.
    """
    def test_create_task_as_authenticated_user(self, authenticated_client, user):
        url = reverse('tasks-list')
        valid_data = {
            'name': 'Test task',
            'description': 'Test description',
            'owner': user.username,
            'assigned_to': user.username,
            'completed': False
        }
        response = authenticated_client.post(url, data=valid_data)
        assert response.status_code == 201
        assert Task.objects.count() == 1
        task = Task.objects.get(pk=1)
        response_data = dict(response.data)
        del response_data['id']
        for k, v in response_data.items():
            # compare returned data with posted
            assert valid_data[k] == v
            # compare model data with posted
            assert str(getattr(task, k)) == str(v)

    def test_mark_task_completed_by_owner(self, authenticated_client, task):
        url = reverse('tasks-detail', kwargs={'pk': task.pk})
        response = authenticated_client.get(url)
        assert response.data['completed'] is False
        valid_data = {'completed': 'true'}
        # here for patch method you must define content_type
        response = authenticated_client.patch(url, content_type='application/json', data=valid_data)
        assert response.status_code == 200
        assert response.data['completed'] is True

    def test_assign_task(self, authenticated_client, task, user, user2):
        url = reverse('tasks-detail', kwargs={'pk': task.pk})
        response = authenticated_client.get(url)
        assert response.data['assigned_to'] == user2.username
        valid_data = {'assigned_to': user.username}
        response = authenticated_client.patch(url, content_type='application/json', data=valid_data)
        assert response.status_code == 200
        assert response.data['assigned_to'] == user.username


@pytest.mark.django_db
class TestTaskViewSetJwtAuth:
    """
    Test class for endpoints of the TaskViewSet when accessed with JWT token
    """
    def test_create_task_as_authenticated_user_jwt(self, authenticated_api_client, user):
        url = reverse('tasks-list')
        valid_data = {
            'name': 'Test task',
            'description': 'Test description',
            'owner': user.username,
            'assigned_to': user.username,
            'completed': False
        }
        response = authenticated_api_client.post(url, data=valid_data)
        assert response.status_code == 201
        assert Task.objects.count() == 1
        task = Task.objects.get(pk=1)
        response_data = dict(response.data)
        del response_data['id']
        for k, v in response_data.items():
            # compare returned data with posted
            assert valid_data[k] == v
            # compare model data with posted
            assert str(getattr(task, k)) == str(v)

    def test_mark_task_completed_by_owner_jwt(self, authenticated_api_client, task):
        url = reverse('tasks-detail', kwargs={'pk': task.pk})
        response = authenticated_api_client.get(url)
        assert response.data['completed'] is False
        valid_data = {'completed': 'true'}
        # here for patch method you must not define content type
        response = authenticated_api_client.patch(url, data=valid_data)
        print(response.data)
        assert response.status_code == 200
        assert response.data['completed'] is True

    def test_assign_task_jwt(self, authenticated_api_client, task, user, user2):
        url = reverse('tasks-detail', kwargs={'pk': task.pk})
        response = authenticated_api_client.get(url)
        assert response.data['assigned_to'] == user2.username
        valid_data = {'assigned_to': user.username}
        response = authenticated_api_client.patch(url, data=valid_data)
        assert response.status_code == 200
        assert response.data['assigned_to'] == user.username
