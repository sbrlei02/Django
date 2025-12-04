"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from Moods.views import MoodListCreateAPIView, MoodRetrieveUpdateDestroyAPIView, mood_history, mood_analytics
from Motivation.views import MotivationListCreateAPIView, MotivationRetrieveUpdateDestroyAPIView
from Post.views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, CommentRetrieveUpdateDestroyAPIView, get_post_comments, create_comment
from Users.views import UserViewSet, UserAccountViewSet
from core.views import register, verify_email

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'useraccounts', UserAccountViewSet)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', register, name='register'),
    path('api/verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),
    path('admin/', admin.site.urls),
    path('api/moods/', MoodListCreateAPIView.as_view(), name='mood-list-create'),
    path('api/mood-history/', mood_history, name='mood-history'),
    path('api/mood-analytics/', mood_analytics, name='mood-analytics'),
    path('api/motivation/', MotivationListCreateAPIView.as_view(), name='motivation-list-create'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
    path('api/posts/<int:post_pk>/comments/', get_post_comments, name='post-comments'),
    path('api/posts/<int:post_pk>/comments/create/', create_comment, name='create-comment'),
    path('api/posts/<int:post_pk>/comments/<int:comment_pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    