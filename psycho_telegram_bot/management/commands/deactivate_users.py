from django.core.management.base import BaseCommand
from app.deactivate_users import deactivate_users

class Command(BaseCommand):
    help = 'Deactivates users whose last payment was more than 30 days ago.'

    def handle(self, *args, **kwargs):
        deactivate_users()
