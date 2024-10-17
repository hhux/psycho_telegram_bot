from datetime import timedelta

from rest_framework import generics
from datetime import datetime, timedelta
from django.utils import timezone

from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


def check_user_status() -> None:
    """
    Запрашивает список пользователей, чтобы проверить их статус и деактивировать пользователей у
    которых дата последней оплаты была больше >30 дней назад.
    """

    # Calculate the date 30 days ago from now
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)

    # Fetch users whose last payment date is older than 30 days
    inactive_users = User.objects.filter(last_payment_date__lt=thirty_days_ago, is_active=True)

    # Deactivate those users
    inactive_users.update(is_active=False)
