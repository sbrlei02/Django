from django.shortcuts import render

# Create your views here.
from .models import Mood
from .serializers import MoodSerializer
from rest_framework import generics

class MoodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

class MoodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer