# models.py
from django.db import models
import uuid
import random


class User(models.Model):
    user_id = models.BigIntegerField(unique=True)
    last_payment = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    comment = models.CharField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.comment:
            self.comment = self.generate_unique_comment()
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_comment():
        return str(random.randint(100000, 999999))
