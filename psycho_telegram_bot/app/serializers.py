from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import User


class UserSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'last_payment', 'is_active', 'comment']

