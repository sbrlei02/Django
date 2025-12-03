from rest_framework import serializers
from .models import User, UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']

class UserAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserAccount
        fields = ['user', 'account_type', 'is_active', 'created_at']