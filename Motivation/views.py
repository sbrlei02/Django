from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Motivation
from .serializers import MotivationSerializer

class MotivationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Motivation.objects.all()
    serializer_class = MotivationSerializer

class MotivationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motivation.objects.all()
    serializer_class = MotivationSerializer 