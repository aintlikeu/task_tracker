from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.permissions import IsAdminOrOwner


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (AllowAny,)
        elif self.action == 'destroy':
            permission_classes = (IsAdminOrOwner,)
        elif self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated,)
        elif self.action == 'change_password':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(
            username=serializer.validated_data['username'],
            password=password)
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = CustomUser.objects.get(pk=request.user.pk)
        password = request.data.get('password', None)
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': 'password was changed'}, status=status.HTTP_204_NO_CONTENT)
