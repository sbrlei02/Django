from django.shortcuts import render
from rest_framework import viewsets
from .models import User, UserAccount
from .serializers import UserSerializer, UserAccountSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def perform_create(self, serializer):
        serializer.save()