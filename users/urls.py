from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('', index, name='index'),
    
    path('register/', CustomUserCreateView.as_view(), name='create-user'),
    # path('', include('djoser.urls.jwt')),
    path('activate/', CustomActivationView.as_view(), name='activate'),
    path('resend-otp/', ResendOTPView.as_view(), name='send-otp'),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('', include('djoser.social.urls')),
    path('', include('djoser.urls')),
]