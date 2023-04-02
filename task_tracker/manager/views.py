from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from manager.models import Task
from manager.serializers import TaskSerializer
from manager.permissions import IsOwnerOrReadOnly, IsOwnerOrAssignedTo
from manager.services import user_exist
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    @action(detail=True, methods=['post'], permission_classes=(IsOwnerOrAssignedTo,))
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'message': 'Task marked as completed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=(IsOwnerOrAssignedTo,))
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.completed = False
        task.save()
        return Response({'message': 'Task marked as not completed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=(IsOwnerOrAssignedTo,))
    def delegate(self, request, pk=None):
        task = self.get_object()
        user = user_exist(request.data['assigned_to'])
        if user:
            task.assigned_to = user
            task.save()
            return Response({'message': 'Task was delegated'}, status=status.HTTP_200_OK)
