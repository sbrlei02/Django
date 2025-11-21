from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from Motivation.views import (
    MotivationListCreateAPIView,
    MotivationRetrieveUpdateDestroyAPIView,
)
from Post.views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
)
from Users.views import (
    UserListCreateAPIView, 
    UserRetrieveUpdateDestroyAPIView,
)
from Moods.views import (
    MoodListCreateAPIView,
    MoodRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/motivation/', MotivationListCreateAPIView.as_view(), name='motivation-list-create'),
    path('api/post/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/users/', UserListCreateAPIView.as_view(), name='users-list-create'),
    path('api/moods/', MoodListCreateAPIView.as_view(), name='moods-list-create'),
]
