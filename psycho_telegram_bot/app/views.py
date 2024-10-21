from datetime import timedelta, datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import logging
from rest_framework.decorators import api_view
from rest_framework import generics
from datetime import datetime, timedelta
from django.utils import timezone
from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deactivate_users(request) -> Response:
    # Определяем дату 30 дней назад
    threshold_date = datetime.now() - timedelta(days=30)
    
    # Запрашиваем пользователей, у которых дата оплаты более 30 дней назад или отсутствует
    users_to_deactivate = User.objects.filter(
        last_payment__lt=threshold_date
    ) | User.objects.filter(last_payment__isnull=True)
    
    # Деактивируем пользователей и получаем количество
    total_count = users_to_deactivate.update(is_active=False)
    
    # Логируем количество деактивированных пользователей
    logger.info(f"Total deactivated users: {total_count}")

    return total_count

