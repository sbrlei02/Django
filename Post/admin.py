from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
