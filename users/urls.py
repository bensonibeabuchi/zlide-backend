
from django.urls import path, include
from.views import *


urlpatterns = [
    path('', index, name='index'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
]