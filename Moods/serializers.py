from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mood

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = '__all__'
        read_only_fields = ('logged_at',)

class MoodAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'mood', 'happy', 'sad', 'angry', 'excited', 'anxious', 'logged_at']