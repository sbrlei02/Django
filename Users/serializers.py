from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class UserAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserAccount
        fields = ['user', 'account_type', 'profile_picture', 'bio', 'is_active', 'created_at']