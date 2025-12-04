from django.contrib import admin
from .models import UserAccount

# Register your models here.
@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at']