from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token
    
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            password_confirmation = serializers.CharField(write_only=True)
            model = User
            fields = ('id', 'username', 'password', 'password_confirmation')
            extra_kwargs = {
                'password': {'write_only': True},
            }
            
            def create(self, validated_data):
                if validated_data('password') != validated_data('password_confirmation'):
                    raise serializers.validationError('Password does not match')
                return super().create(validated_data)