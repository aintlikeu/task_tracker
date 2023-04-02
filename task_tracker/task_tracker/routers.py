from rest_framework import routers
from manager.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/tasks', TaskViewSet, basename='tasks')
