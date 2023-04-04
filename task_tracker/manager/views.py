from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from manager.models import Task
from manager.serializers import TaskSerializer
from manager.permissions import IsOwnerOrAssignedTo


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAssignedTo, )

    def update(self, request, *args, **kwargs):
        """
        Overriding update method to exclude read only fields 'name' and 'owner'
        """
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs['partial'])
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        read_only_fields = ('name', 'owner')
        for field in read_only_fields:
            validated_data.pop(field, None)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
