from rest_framework import serializers
from .models import Motivation

class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = '__all__'