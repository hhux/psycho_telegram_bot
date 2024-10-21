import logging
from datetime import datetime, timedelta
from .models import User

# Настраиваем логгер
logger = logging.getLogger(__name__)


def deactivate_users():
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
