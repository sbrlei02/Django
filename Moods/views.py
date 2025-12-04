from django.shortcuts import render
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Mood
from .serializers import MoodSerializer, MoodAnalyticsSerializer

class MoodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class MoodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

@api_view(['GET'])
def mood_history(request):
    """
    Get mood history for authenticated user with date grouping
    """
    if request.user.is_authenticated:
        user_moods = Mood.objects.filter(user=request.user).order_by('-logged_at')
    else:
        user_id = request.query_params.get('user_id', None)
        if user_id:
            user_moods = Mood.objects.filter(user_id=user_id).order_by('-logged_at')
        else:
            return Response({'error': 'User not authenticated and no user_id provided'},
                          status=status.HTTP_400_BAD_REQUEST)

    serializer = MoodAnalyticsSerializer(user_moods, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def mood_analytics(request):
    if request.user.is_authenticated:
        user_moods = Mood.objects.filter(user=request.user)
        user_info = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        }
    else:
        user_id = request.query_params.get('user_id', None)
        if user_id:
            user_moods = Mood.objects.filter(user_id=user_id)
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(id=user_id)
                user_info = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not authenticated and no user_id provided'},
                          status=status.HTTP_400_BAD_REQUEST)

    # Calculate mood statistics based on mood history
    mood_stats = {
        'total_entries': user_moods.count(),
        'happy_count': user_moods.filter(happy=True).count(),
        'sad_count': user_moods.filter(sad=True).count(),
        'angry_count': user_moods.filter(angry=True).count(),
        'excited_count': user_moods.filter(excited=True).count(),
        'anxious_count': user_moods.filter(anxious=True).count(),
        'date_range': {
            'first_entry': user_moods.order_by('logged_at').first().logged_at if user_moods.exists() else None,
            'latest_entry': user_moods.order_by('-logged_at').first().logged_at if user_moods.exists() else None
        }
    }

    total_moods = user_moods.count()
    mood_distribution = {}
    if total_moods > 0:
        mood_distribution = {
            'happy': {
                'count': user_moods.filter(happy=True).count(),
                'percentage': round((user_moods.filter(happy=True).count() / total_moods) * 100, 2)
            },
            'sad': {
                'count': user_moods.filter(sad=True).count(),
                'percentage': round((user_moods.filter(sad=True).count() / total_moods) * 100, 2)
            },
            'angry': {
                'count': user_moods.filter(angry=True).count(),
                'percentage': round((user_moods.filter(angry=True).count() / total_moods) * 100, 2)
            },
            'excited': {
                'count': user_moods.filter(excited=True).count(),
                'percentage': round((user_moods.filter(excited=True).count() / total_moods) * 100, 2)
            },
            'anxious': {
                'count': user_moods.filter(anxious=True).count(),
                'percentage': round((user_moods.filter(anxious=True).count() / total_moods) * 100, 2)
            }
        }
    else:
        mood_distribution = {
            'happy': {'count': 0, 'percentage': 0},
            'sad': {'count': 0, 'percentage': 0},
            'angry': {'count': 0, 'percentage': 0},
            'excited': {'count': 0, 'percentage': 0},
            'anxious': {'count': 0, 'percentage': 0}
        }

    # Calculate mood consistency (how regularly user logs moods)
    if user_moods.exists():
        first_date = user_moods.order_by('logged_at').first().logged_at.date()
        last_date = user_moods.order_by('-logged_at').first().logged_at.date()
        total_days = (last_date - first_date).days + 1
        days_with_entries = user_moods.dates('logged_at', 'day').count()
        consistency = round((days_with_entries / total_days) * 100, 2) if total_days > 0 else 0
    else:
        consistency = 0

    # Most common mood (mood count per day, like ilang beses nya nafeel yung isang mood)
    mood_counts = []
    for mood_type in ['happy', 'sad', 'angry', 'excited', 'anxious']:
        count = user_moods.filter(**{mood_type: True}).count()
        mood_counts.append({'mood': mood_type, 'count': count})

    most_common_mood = max(mood_counts, key=lambda x: x['count']) if mood_counts else {'mood': 'none', 'count': 0}

    # Find dates with dominant moods (layk kung ano yung pinaka maraming nafeel na mood per day)
    dominant_mood_by_date = []
    for mood_date in user_moods.dates('logged_at', 'day'):
        date_moods = user_moods.filter(logged_at__date=mood_date)
        daily_mood_counts = []
        for mood_type in ['happy', 'sad', 'angry', 'excited', 'anxious']:
            count = date_moods.filter(**{mood_type: True}).count()
            daily_mood_counts.append({'mood': mood_type, 'count': count})

        # Find the dominant mood for this date
        dominant = max(daily_mood_counts, key=lambda x: x['count'])
        if dominant['count'] > 0:  
            dominant_mood_by_date.append({
                'date': mood_date.strftime('%Y-%m-%d'),
                'dominant_mood': dominant['mood'],
                'count': dominant['count'],
                'total_entries': date_moods.count()
            })

    analytics_data = {
        'user': user_info,
        'mood_stats': mood_stats,
        'mood_distribution': mood_distribution,
        'consistency_percentage': consistency,
        'most_common_mood': most_common_mood,
        'total_moods': total_moods,
        'dominant_mood_by_date': dominant_mood_by_date
    }

    return Response(analytics_data)