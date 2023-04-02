from django.shortcuts import get_object_or_404
from accounts.models import CustomUser


def user_exist(username):
    user = get_object_or_404(CustomUser, username=username)
    return user
