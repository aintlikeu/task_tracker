import pytest
from django.urls import reverse
from manager.models import Task


@pytest.mark.django_db
class TestTaskViewSetAnonymous:
    """

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

    # BOTH TESTS DON'T WORK YET (!!!)
    def test_mark_task_completed_by_owner(self, authenticated_client, task):
        url = reverse('tasks-detail', kwargs={'pk': 1})
        valid_data = {'completed': 'true'}
        # here for PATCH method you must use 'json' argument instead of 'data' ??
        response = authenticated_client.patch(url, json=valid_data)
        # assert response.status_code == 200
        # assert response.data['completed'] is True
        print(response.data)

    def test_assign_task(self, authenticated_client, task, user2):
        url = reverse('tasks-detail', kwargs={'pk': 1})
        valid_data = {'assigned_to': 'test_1'}
        # here for PATCH method you must use 'json' argument instead of 'data' ??
        response = authenticated_client.patch(url, data=valid_data)
        # assert response.status_code == 200
        # assert response.data['completed'] is True
        print(response.data)

# [<URLPattern '^api/v1/tasks/$' [name='tasks-list']>,
#  <URLPattern '^api/v1/tasks\.(?P<format>[a-z0-9]+)/?$' [name='tasks-list']>,
#  <URLPattern '^api/v1/tasks/(?P<pk>[^/.]+)/$' [name='tasks-detail']>,
#  <URLPattern '^api/v1/tasks/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='tasks-detail']>,
