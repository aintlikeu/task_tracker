from rest_framework import routers
from manager.views import TaskViewSet
from accounts.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/tasks', TaskViewSet, basename='tasks')
router.register(r'api/v1/users', CustomUserViewSet, basename='users')
