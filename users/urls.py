from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path("auth/logout/", LogoutView.as_view(), name='logout'),
    # path('register/', UserRegistrationAPIView.as_view(), name='register'),
    # path('user/<int:id>', UserDetailView.as_view(), name='user-detail')
]