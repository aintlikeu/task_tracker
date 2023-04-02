from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from manager.models import Task
from manager.serializers import TaskSerializer
from manager.permissions import IsOwnerOrReadOnly, IsOwnerOrAssignedTo
from accounts.models import CustomUser


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

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
        assigned_to = request.data.get('assigned_to')
        if assigned_to:
            user = get_object_or_404(CustomUser, username=assigned_to)
            task.assigned_to = user
            task.save()
            return Response({'message': 'Task was delegated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'assigned_to field is required'}, status=status.HTTP_400_BAD_REQUEST)
