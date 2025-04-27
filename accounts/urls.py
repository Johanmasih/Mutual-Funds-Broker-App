from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('api/v1/login', TokenObtainPairView.as_view(), name='login'),   # Login to get tokens
    path('api/v1/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),  # Refresh access token
    path('api/v1/register-user', RegisterView.as_view(), name='register_user'),  # Register a new user
    path('api/v1/logout-user', LogoutView.as_view(), name='logout_user'),  # Logout and blacklist token
]