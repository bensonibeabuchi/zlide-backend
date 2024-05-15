from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('', index, name='index'),
    path('users/', CustomUserCreateView.as_view(), name='user-create'),
    path('activate/', CustomActivationView.as_view(), name='activate'),
    path('resend-otp/', SendOTPView.as_view(), name='send-otp'),
    path('', include('djoser.urls')),
    path('', include('djoser.social.urls')),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]