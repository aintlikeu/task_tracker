from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from accounts.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')
