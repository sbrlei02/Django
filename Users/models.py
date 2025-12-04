from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_type = models.CharField(
        max_length=20,
        default='normal',
        choices=[
            ('normal', 'Normal'),
            ('admin', 'Admin'),
        ]
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Account"