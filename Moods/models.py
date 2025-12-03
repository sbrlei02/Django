from django.db import models

# Create your models here.
class Mood(models.Model):
    mood = models.CharField(max_length=100)
    happy = models.BooleanField(default=False)
    sad = models.BooleanField(default=False)
    angry = models.BooleanField(default=False)
    excited = models.BooleanField(default=False)
    anxious = models.BooleanField(default=False)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mood    
    
    

    