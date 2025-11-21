from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Mood
from .serializers import MoodSerializer
from django.shortcuts import get_object_or_404

class MoodListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsAuthenticated]           

    def get(self, request):
        moods = Mood.objects.all()
        serializer = MoodSerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mood = get_object_or_404(Mood, pk=pk)
        serializer = MoodSerializer(mood)
        return Response(serializer.data)

    def put(self, request, pk):
        mood = get_object_or_404(Mood, pk=pk)
        serializer = MoodSerializer(mood, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mood = get_object_or_404(Mood, pk=pk)
        mood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
