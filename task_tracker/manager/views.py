from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from manager.models import Task
from manager.serializers import TaskSerializer
from manager.permissions import IsOwnerOrAssignedOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrAssignedOrReadOnly, )

    # def get_queryset(self):
    #     user = self.request.user
    #     return Task.objects.filter(Q(owner=user) | Q(assigned_to=user)).order_by('id')
