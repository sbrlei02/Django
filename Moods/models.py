from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moods', null=True, blank=True)
    mood = models.CharField(max_length=100)
    happy = models.BooleanField(default=False)
    sad = models.BooleanField(default=False)
    angry = models.BooleanField(default=False)
    excited = models.BooleanField(default=False)
    anxious = models.BooleanField(default=False)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood} - {self.logged_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-logged_at']    
    
    

    