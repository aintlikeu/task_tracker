from rest_framework.serializers import ModelSerializer
from manager.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
