from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ProfileView, UserViewSet

# Router setup for user viewset (handles follow/unfollow, followers, following)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Include router-generated endpoints (/users/, /users/<id>/follow/, etc.)
    path('', include(router.urls)),
]
