from rest_framework.views import APIView
from django.contrib.auth.models import Users
from .serializers import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class UserView(APIView):
    
    
    
    def get(self , request, format=None):
        users = Users.objects.all()
        serializer = serializers(users, many=True)
        return Response({'ok': True, 'data': serializer.data} , status=200)